import requests
import json

def fetch_commit_details(repo, sha, lsttokens, ct):
    """
    Fetches commit details from the GitHub API for a specific commit SHA.
    
    Args:
        repo (str): The GitHub repository name in the format "owner/repo".
        sha (str): The SHA hash of the commit to retrieve details for.
        lsttokens (list): A list of GitHub authentication tokens used for API requests.
        ct (int): The current index of the authentication token being used.

    Returns:
        tuple: (filesjson, author, date, ct)
            - filesjson (list): A list of file objects modified in the commit.
            - author (str): The name of the commit author.
            - date (str): The date and time of the commit in ISO 8601 format.
            - ct (int): The updated authentication token index.
    """
    # Construct the GitHub API URL for the commit details
    sha_url = f'https://api.github.com/repos/{repo}/commits/{sha}'

    # Authenticate and fetch commit details
    sha_details, ct = github_auth(sha_url, lsttokens, ct)

    # Check if the API response contains data
    if not sha_details:
        return None, None, None, ct  # Handle cases where API call fails

    # Extract commit files, author name, and commit date
    filesjson = sha_details.get('files', [])  # List of files modified in this commit
    author = sha_details.get('commit', {}).get('author', {}).get('name', 'Unknown')  # Author name
    date = sha_details.get('commit', {}).get('author', {}).get('date', None)  # Commit timestamp

    return filesjson, author, date, ct


def countfiles(dictfiles, lsttokens, repo):
    """
    Fetches the commit history of a GitHub repository and tracks the authorship 
    and modification timestamps of selected source files.
    
    Args:
        dictfiles (dict): A dictionary where keys are filenames and values are 
                          lists of tuples containing (author, date) information.
        lsttokens (list): A list of GitHub authentication tokens for API requests.
        repo (str): The GitHub repository name in the format "owner/repo".

    Returns:
        None: Updates dictfiles in place.
    
    Raises:
        requests.RequestException: If an error occurs during an HTTP request.
        json.JSONDecodeError: If the JSON response cannot be parsed correctly.
        KeyError: If an expected key is missing from the API response.
    """
    ipage = 1  # Page counter for paginated API responses
    ct = 0  # Token counter for authentication cycling

    try:
        while True:  # Loop through commit pages until an empty response is received
            # Construct the URL to fetch a page of commits
            commits_url = f'https://api.github.com/repos/{repo}/commits?page={ipage}&per_page=100'

            # Fetch the list of commits for the current page
            json_commits, ct = github_auth(commits_url, lsttokens, ct)

            # Break if no more commits exist (i.e., end of pagination)
            if not json_commits:
                break

            # Iterate through each commit in the current page
            for sha_object in json_commits:
                sha = sha_object.get('sha')  # Extract the commit SHA hash
                if not sha:
                    continue  # Skip if SHA is missing

                # Fetch commit details, including files modified, author, and date
                filesjson, author, date, ct = fetch_commit_details(repo, sha, lsttokens, ct)
                
                # Skip this commit if we failed to retrieve essential data
                if not filesjson or not author or not date:
                    continue

                # Iterate through the list of modified files in the commit
                for file_obj in filesjson:
                    filename = file_obj.get('filename')  # Extract filename
                    
                    # Only process files that are in the predefined list "source_files"
                    if filename in source_files:
                        # Add author and date to the dictionary entry for this file
                        dictfiles.setdefault(filename, []).append((author, date))

            # Move to the next page of commits
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
