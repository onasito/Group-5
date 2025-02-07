# Jaison-Noah Sarte - Lab 1 Git & Github
# CS 472 - Spring 2025
# Date: 1/26/2025

import json
import requests
import os
import csv

# My github token
token = ["11212"]

# Checking if file is source file
def source_file(file):
    sourceFiles = [".cpp", ".kt", ".java", ".xml"] # Only source files I seen in repo
    if any(file.endswith(type) for type in sourceFiles):
        return True
    return False

# GitHub Authentication function
def github_auth(url, token, ct):
    jsonData = None
    try:
        ct = ct % len(token)
        headers = {'Authorization': 'Bearer {}'.format(token[ct])}
        request = requests.get(url, headers=headers)
        jsonData = json.loads(request.content)
        ct += 1
    except Exception as e:
        pass
        print(e)
    return jsonData, ct


# @dictFiles, empty dictionary of files
# @lstTokens, GitHub authentication tokens
# @repo, GitHub repo
def get_file_data(token, repo):
    ipage = 1  # url page counter
    ct = 0  # token counter
    authorDates = {} # dictionary of authors and their commit dates

    try:
        # loop though all the commit pages until the last returned empty page
        while True:
            spage = str(ipage)
            commitsUrl = 'https://api.github.com/repos/' + repo + '/commits?page=' + spage + '&per_page=100'
            jsonCommits, ct = github_auth(commitsUrl, token, ct)

            # break out of loop if no commits on page
            if len(jsonCommits) == 0:
                break

            # iterate through the list of commits in  spage
            for shaObject in jsonCommits:
                sha = shaObject['sha']

                # For each commit, use the GitHub commit API to extract the files touched by the commit
                shaUrl = 'https://api.github.com/repos/' + repo + '/commits/' + sha
                shaDetails, ct = github_auth(shaUrl, token, ct)

                # Grab author and date of commit
                # Gets the author name in dictionary, if not found, use "Missing Name"
                authorData = shaDetails.get("commit", {}).get("author", {}).get("name", "Missing Name")
                # Gets the author date in dictionary, if not found, use "Missing Date"
                dateData = shaDetails.get("commit", {}).get("author", {}).get("date", "Missing Date")
                # Get the files touched by the commit
                filesjson = shaDetails.get("files", [])

                for filenameObj in filesjson:
                    filename = filenameObj["filename"]
                    # Checking if file is a source file (.cpp, .kt, .java, .xml)
                    if source_file(filename):
                        # Checking if in the dictionary
                        if filename not in authorDates:
                            authorDates[filename] = []
                        authorDates[filename].append((authorData, dateData))
            ipage += 1
    except:
        print("Error receiving data")
        exit(0)

    return authorDates

# GitHub repo
repo = 'scottyab/rootbeer'
# Get the author and date of the files
repoData = get_file_data(token, repo)

# Write to csv file
with open("data/data_rootbeer.csv", "w", newline="", encoding="utf-8") as csvFile:
    # csv writer object to write to csv file
    writer = csv.writer(csvFile)
    # Write the headers
    writer.writerow(["File", "Author", "Date"])

    # Write the data to the csv file
    for file, data in repoData.items():
        for author, date in data:
            writer.writerow([file, author, date])

print("Author and Date data written to data/data_rootbeer.csv")