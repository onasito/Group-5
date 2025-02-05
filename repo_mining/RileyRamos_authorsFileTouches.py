import json
import requests
import csv
import os

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

# @filesList, empty list of files
# @lstTokens, GitHub authentication tokens
# @repo, GitHub repo
def getAuthorDate(filesList, lsttokens, repo):
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
                # get commit 
                commits = shaDetails['commit']
                # get files from commit
                filesjson = shaDetails['files']
                # for each commit, get the author and date
                author = commits['author']['name']
                # print(commits['author']['name'])
                date = commits['author']['date']
                # print(commits['author']['date'])
                # for each commit, get the list of file names
                files = []
                for filenameObj in filesjson:
                    filename = filenameObj['filename']
                    # only get source files 
                    if 'src' in filename:
                        files.append(filename)
                # gather commit info for that file and append to list
                for file in files:
                    commitInfo = (file, author, date)
                    filesList.append(commitInfo)
            ipage += 1
    except:
        print("Error receiving data")
        exit(0)

# GitHub repo
repo = 'scottyab/rootbeer'

# Tokens - REMOVE BEFORE COMMITTING
lstTokens = [""]

# Initialize files list & gather commit info 
filesList = []
getAuthorDate(filesList, lstTokens, repo)

# Write to CSV file
fileOutput = 'data/file_authorDate.csv'
rows = ["Filename", "Author", "Date"]
fileCSV = open(fileOutput, 'w')
writer = csv.writer(fileCSV)
writer.writerow(rows)

for commit in filesList:
    rows = [commit[0], commit[1], commit[2]]
    writer.writerow(rows)

fileCSV.close()