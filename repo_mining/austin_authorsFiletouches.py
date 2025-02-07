import json
import requests
import os

# List of source files to process
source_files = [
    "app/src/main/java/com/scottyab/rootbeer/sample/CheckForRootWorker.kt",
    "app/src/main/java/com/scottyab/rootbeer/sample/MainActivity.kt",
    "app/src/main/java/com/scottyab/rootbeer/sample/RootItemResult.kt",
    "app/src/main/java/com/scottyab/rootbeer/sample/RootSampleApp.kt",
    "app/src/main/java/com/scottyab/rootbeer/sample/extensions/ViewExtensions.kt",
    "app/src/main/java/com/scottyab/rootbeer/sample/ui/ResultIconView.kt",
    "app/src/main/java/com/scottyab/rootbeer/sample/ui/RootItemAdapter.kt",
    "app/src/main/java/com/scottyab/rootbeer/sample/ui/RootedResultTextView.kt",
    "app/src/main/java/com/scottyab/rootbeer/sample/ui/ScopedActivity.kt",
    "rootbeerlib/src/main/java/com/scottyab/rootbeer/util/Utils.java",
    "rootbeerlib/src/main/java/com/scottyab/rootbeer/RootBeerNative.java",
    "rootbeerlib/src/main/cpp/toolChecker.cpp",
    "app/src/main/java/com/scottyab/rootbeer/sample/CheckRootTask.java",
    "app/src/main/java/com/scottyab/rootbeer/sample/MainActivity.java",
    "app/src/main/java/com/scottyab/rootbeer/sample/TextViewFont.java",
    "rootbeerlib/src/main/java/com/scottyab/rootbeer/Const.java",
    "rootbeerlib/src/main/java/com/scottyab/rootbeer/RootBeer.java",
    "rootbeerlib/src/main/java/com/scottyab/rootbeer/util/QLog.java",
    "rootbeerlib/src/main/jni/toolChecker.cpp",
    "rootbeerlib/jni/toolChecker.cpp",
    "app/src/main/java/com/scottyab/rootchecker/RootCheck.java",
    "app/src/main/java/com/scottyab/rootchecker/Const.java",
    "app/src/main/java/com/scottyab/rootchecker/MainActivity.java",
    "app/jni/toolChecker.cpp",
    "app/src/main/java/com/scottyab/rootchecker/RootCheckNative.java",
    "app/jni/rootChecker.cpp",
    "app/src/main/java/com/scottyab/rootchecker/util/QLog.java"
]

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
def countfiles(dictfiles, lsttokens, repo):
    ipage = 1  # url page counter
    ct = 0  # token counter

    try:
        # loop through all the commit pages until the last returned empty page
        while True:
            spage = str(ipage)
            commitsUrl = 'https://api.github.com/repos/' + repo + '/commits?page=' + spage + '&per_page=100'
            jsonCommits, ct = github_auth(commitsUrl, lsttokens, ct)

            # break out of the while loop if there are no more commits in the pages
            if len(jsonCommits) == 0:
                break
            # iterate through the list of commits in spage
            for shaObject in jsonCommits:
                sha = shaObject['sha']
                # For each commit, use the GitHub commit API to extract the files touched by the commit
                shaUrl = 'https://api.github.com/repos/' + repo + '/commits/' + sha
                shaDetails, ct = github_auth(shaUrl, lsttokens, ct)
                filesjson = shaDetails['files']
                author = shaDetails['commit']['author']['name']
                date = shaDetails['commit']['author']['date']

                for filenameObj in filesjson:
                    filename = filenameObj['filename']
                    # Only process the source files in the list above 
                    if filename in source_files:
                        # if the filename is not already in the dictionary, then add to it
                        if filename not in dictfiles:
                            dictfiles[filename] = []
                        # the filename is the key and the author & date of the commit are values 
                        dictfiles[filename].append((author, date))

            ipage += 1
    except:
        print("Error receiving data")
        exit(0)

# GitHub repo
repo = 'scottyab/rootbeer'
# repo = 'Skyscanner/backpack' # This repo is commit heavy. It takes long to finish executing
# repo = 'k9mail/k-9' # This repo is commit heavy. It takes long to finish executing
# repo = 'mendhak/gpslogger'

# put your tokens here
# Remember to empty the list when going to commit to GitHub.
# Otherwise they will all be reverted and you will have to re-create them
# I would advise to create more than one token for repos with heavy commits
lstTokens = [""]

dictfiles = dict()
countfiles(dictfiles, lstTokens, repo)
print('Total number of source files: ' + str(len(dictfiles)))

# Print commit history for each file
for filename, author_commit in dictfiles.items():
    print(f"File Name: {filename}")
    print("-" * 80)
    for author, date in author_commit:
        print(f"Commit Author: {author} Date of Commit: {date}")
    print()  