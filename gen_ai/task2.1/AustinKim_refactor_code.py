# Changes & Benefits:
# Extracted API calls: The fetch_commit_details function prevents redundant calls inside countfiles, making the code cleaner.
# Improved error handling: Catches specific exceptions and avoids except: which masks debugging issues.
# Better dictionary operations: Uses .setdefault() for cleaner list initialization.
# Safer JSON parsing: Uses .get() to avoid KeyError crashes.

def fetch_commit_details(repo, sha, lsttokens, ct):
    """Fetches commit details including the author, date, and files changed for a given commit SHA."""
    sha_url = f'https://api.github.com/repos/{repo}/commits/{sha}'
    sha_details, ct = github_auth(sha_url, lsttokens, ct)

    if not sha_details:
        return None, None, None, ct  # Handle cases where API call fails

    filesjson = sha_details.get('files', [])
    author = sha_details.get('commit', {}).get('author', {}).get('name', 'Unknown')
    date = sha_details.get('commit', {}).get('author', {}).get('date', None)

    return filesjson, author, date, ct

def countfiles(dictfiles, lsttokens, repo):
    """Fetches commit history and tracks authorship of selected source files."""
    ipage = 1  
    ct = 0  

    try:
        while True:
            commits_url = f'https://api.github.com/repos/{repo}/commits?page={ipage}&per_page=100'
            json_commits, ct = github_auth(commits_url, lsttokens, ct)

            if not json_commits:  
                break

            for sha_object in json_commits:
                sha = sha_object.get('sha')
                if not sha:
                    continue

                filesjson, author, date, ct = fetch_commit_details(repo, sha, lsttokens, ct)
                if not filesjson or not author or not date:
                    continue  

                for file_obj in filesjson:
                    filename = file_obj.get('filename')
                    if filename in source_files:
                        dictfiles.setdefault(filename, []).append((author, date))

            ipage += 1
    except requests.RequestException as req_err:
        print(f"Request error: {req_err}")
        exit(1)
    except json.JSONDecodeError as json_err:
        print(f"JSON decoding error: {json_err}")
        exit(1)
    except KeyError as key_err:
        print(f"Unexpected JSON structure: Missing key {key_err}")
        exit(1)
