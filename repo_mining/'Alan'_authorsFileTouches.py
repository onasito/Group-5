import json
import requests
import csv
import os

# Directory for storing output data
if not os.path.exists("data"):
    os.makedirs("data")

def github_auth(url, lsttokens, ct):
    jsonData = None
    try:
        ct = ct % len(lsttokens)
        headers = {'Authorization': f'Bearer {lsttokens[ct]}'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        jsonData = json.loads(response.content)
        ct += 1
    except Exception as e:
        print(f"Error during GitHub API request: {e}")
    return jsonData, ct

# Collect authors and dates for each file
# @dictFiles: dictionary of files and their touch counts from the previous script
# @lstTokens: list of GitHub authentication tokens
# @repo: GitHub repository in "owner/repo" format
def collect_authors_and_dates(dictfiles, lsttokens, repo):
    authors_dates = {}
    ct = 0

    try:
        for filename in dictfiles.keys():
            authors_dates[filename] = []
            page = 1
            while True:
                commits_url = f'https://api.github.com/repos/{repo}/commits?path={filename}&page={page}&per_page=100'
                json_commits, ct = github_auth(commits_url, lsttokens, ct)

                if not json_commits:
                    break

                for commit in json_commits:
                    author = commit['commit']['author']['name']
                    date = commit['commit']['author']['date']
                    authors_dates[filename].append((author, date))

                page += 1
    except Exception as e:
        print(f"Error collecting authors and dates: {e}")

    return authors_dates

def is_source_file(filename):
    # Define source files as those with common programming file extensions
    source_extensions = {'.py', '.java', '.js', '.cpp', '.c', '.h', '.ts', '.rb', '.go'}
    return any(filename.endswith(ext) for ext in source_extensions)

# GitHub repo
repo = 'scottyab/rootbeer'

# Put your GitHub tokens here
lstTokens = [""]

# Read files and their touches from the previous script's output
input_file = f'data/file_{repo.split("/")[1]}.csv'
dictfiles = {}

with open(input_file, 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip the header row
    for row in reader:
        # Skip rows that are empty or don't have exactly 2 columns
        if len(row) != 2:
            continue
        filename, touches = row
        if is_source_file(filename):
            dictfiles[filename] = int(touches)


# Collect authors and dates
authors_dates = collect_authors_and_dates(dictfiles, lstTokens, repo)

# Write results to a CSV file
output_file = f'data/authors_dates_{repo.split("/")[1]}.csv'
with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Filename", "Author", "Date"])

    for filename, entries in authors_dates.items():
        for author, date in entries:
            writer.writerow([filename, author, date])

print(f"Author and date information has been written to {output_file}.")