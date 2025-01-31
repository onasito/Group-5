import requests
import json
import os
import csv

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

# @files, empty dictionary of files
# @token, GitHub authentication tokens
# @reponame, GitHub repo
def collect_author_and_date(files, token, reponame):
    ipage = 1  # url page counter
    ct = 0  # token counter

    try:
        # loop though all the commit pages until the last returned empty page
        while True:
            spage = str(ipage)
            commitsUrl = 'https://api.github.com/repos/' + reponame + '/commits?page=' + spage + '&per_page=100'
            jsonCommits, ct = github_auth(commitsUrl, token, ct)

            # break out of the while loop if there are no more commits in the pages
            if len(jsonCommits) == 0:
                break
            # iterate through the list of commits in  spage
            for shaObject in jsonCommits:
                sha = shaObject['sha']
                # For each commit, use the GitHub commit API to extract the files touched by the commit
                shaUrl = 'https://api.github.com/repos/' + reponame + '/commits/' + sha
                shaDetails, ct = github_auth(shaUrl, token, ct)
                filesjson = shaDetails['files']
                
                # get author's name and date for each commit
                commits = shaDetails['commit']
                author = commits['author']['name']
                date = commits['author']['date']

                filenames = []
                for filenameObj in filesjson:
                    filename = filenameObj['filename']
                    if any(filename.endswith(ext) for ext in source_file_extensions):
                        filenames.append(filename)
                
                for file in filenames:
                    files.append([file, author, date])
            ipage += 1
    except:
        print("Error receiving data")
        exit(0)

# GitHub repo
reponame = 'scottyab/rootbeer'

# tokens
token = [""]

# file extensions for source files
source_file_extensions = [
    ".pdf",
    ".xml",
    ".html",
    ".css",
    ".log",
    ".txt",
    ".json",
    ".js",
    '.kt',
    '.kts',
    '.sh',
    '.rb',
    '.go',
    '.php',
    '.c',
    '.h',
    '.cs'
]

files = []
collect_author_and_date(files, token, reponame)

# Output authors and dates into a file
fileOutput = 'data/file_rootbeer_authors_and_dates.csv'
fileCSV = open(fileOutput, 'w')
writer = csv.writer(fileCSV)
rows = ['Filename', 'Author', 'Date']
writer.writerow(rows)
writer.writerows(files)
fileCSV.close()
