import json
import requests
from datetime import datetime
import matplotlib.pyplot as plt
from collections import defaultdict
import matplotlib.cm as cm

# List of files from the adjust collectFiles.py
# I added these files into an array because there are some source files that are just used for testing 
files_to_check = [
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

# June 19, 2015 is when scottyab/rootbeer repo was created 
target_date = datetime(2015, 6, 19)

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
                    # Only process files in the files_to_check list
                    if filename in files_to_check:
                        if filename not in dictfiles:
                            dictfiles[filename] = []
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

# This list / hashmap will have author's name as the key and weeks, filename as the values
author_data = defaultdict(list)

# Traverse through the files & commit history 
# Calculate the the week difference used for the scatter plot 
for filename, commit_history in dictfiles.items():
    for author, date in commit_history:
        commit_date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")  
        weeks_since_repo_creation = (commit_date - target_date).days // 7
        author_data[author].append((weeks_since_repo_creation, filename))

fig, ax = plt.subplots(figsize=(12, 8))

# Used to create distinct colors for each point in the scatter plot
colors = cm.get_cmap("tab20", len(author_data))

i = 0
for author, data in author_data.items():
    weeks = [point[0] for point in data]  
    file_counts = [index + 1 for index in range(len(data))]  
    
    ax.scatter(file_counts, weeks, label=author, s=100, color=colors(i))
    i += 1

# Set y-axis intervals to 20 for better visual
y_min, y_max = ax.get_ylim()  
y_ticks = range(int(y_min // 20) * 20, int(y_max // 20 + 1) * 20, 20) 
ax.set_yticks(y_ticks)

ax.set_xlabel('Files Touched', fontsize=12)
ax.set_ylabel('Weeks Since Repo Creation', fontsize=12)
ax.set_title('Source Files Touched by Authors Over Time', fontsize=14)

# Not explicilty mentioned in the instructions, but added this for the scatter plot
# Easier to identify which point corresponds to which author
ax.legend()

plt.show()
