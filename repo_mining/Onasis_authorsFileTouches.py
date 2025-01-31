import json
import requests
import os
import csv

if not os.path.exists("data"):
    os.makedirs("data")

# GitHub Authentication function
def github_auth(url, lsttoken, ct):
    jsonData = None
    try:
        ct = ct % len(lstTokens)
        headers = {'Authorization': 'Bearer {}'.format(lsttoken[ct])}
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
def countfiles(lstFiles, lsttokens, repo):
    ipage = 1  # url page counter
    ct = 0  # token counter

    try:
        # loop though all the commit pages until the last returned empty page
        while True:
            spage = str(ipage)
            commitsUrl = 'https://api.github.com/repos/' + repo + '/commits?page=' + spage + '&per_page=100'
            jsonCommits, ct = github_auth(commitsUrl, lsttokens, ct)

            # break out of the while loop if there are no more commits in the pages
            if len(jsonCommits) == 0:
                break
            # iterate through the list of commits in  spage
            for shaObject in jsonCommits:
                sha = shaObject['sha']
                # For each commit, use the GitHub commit API to extract the files touched by the commit
                shaUrl = 'https://api.github.com/repos/' + repo + '/commits/' + sha
                shaDetails, ct = github_auth(shaUrl, lsttokens, ct)
                filesjson = shaDetails['files']
                touchedFiles = []
                for filenameObj in filesjson:
                    filename = filenameObj['filename']
                    touchedFiles.append(filename)
                if any(filename.endswith(ext) for ext in SOURCE_EXTENSIONS):
                    lstFiles.append((filenameObj['filename'], shaObject['commit']['author']['name'],shaObject['commit']['author']['date']))
            ipage += 1
    except:
        print("Error receiving data")
        exit(0)

# GitHub repo
repo = 'scottyab/rootbeer'

lstTokens = [""] 
lstFiles = []

# Define source file extensions
SOURCE_EXTENSIONS = {".java", ".c", ".cpp", ".h", ".py", ".js", ".ts"}
countfiles(lstFiles,lstTokens, repo)

# Save lstFiles data to a CSV file
csv_filename = "file_data.csv"

with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Filename", "Author", "Date"])  # Write CSV header
    writer.writerows(lstFiles)  # Write all data

print(f"CSV file '{csv_filename}' has been created successfully!")