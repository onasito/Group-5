def countfiles(dictfiles, lsttokens, repo):
    """
    Fetches commit data from a GitHub repository and counts the number of times each file has been modified.
    Additionally, records the authors and timestamps of each modification.

    Parameters:
    - dictfiles (dict): A dictionary to store file modification counts and history.
    - lsttokens (list): List of GitHub authentication tokens for API rate limits.
    - repo (str): The GitHub repository in the format 'owner/repository'.

    Returns:
    - None: Modifies `dictfiles` in-place with file modification data.
    """

    ipage = 1  # Page counter for paginated API requests
    ct = 0  # Token counter for cycling through API tokens

    try:
        while True:
            # [Optimization 1] Fetch maximum commits per page to reduce API calls
            commits_url = f'https://api.github.com/repos/{repo}/commits?page={ipage}&per_page=100'
            
            # Fetch commit data using authentication
            json_commits, ct = github_auth(commits_url, lsttokens, ct)

            # [Optimization 2] Exit early if no more commits are available
            if not json_commits:
                break

            # Process each commit
            for commit_obj in json_commits:
                sha = commit_obj['sha']  # Commit SHA identifier
                
                # Extract author name and date from commit metadata
                author = commit_obj['commit']['author']['name']
                date = commit_obj['commit']['author']['date']

                # Construct the API URL for fetching detailed commit data
                sha_url = f'https://api.github.com/repos/{repo}/commits/{sha}'
                
                # Fetch detailed commit data
                sha_details, ct = github_auth(sha_url, lsttokens, ct)
                
                # [Optimization 3] Handle missing 'files' key gracefully to prevent crashes
                files_json = sha_details.get('files', [])

                for file_obj in files_json:
                    filename = file_obj['filename']  # Extract filename

                    # [Optimization 4] Store modification count and commit history together
                    if filename not in dictfiles:
                        dictfiles[filename] = {'count': 0, 'history': []}

                    # Increment file modification count
                    dictfiles[filename]['count'] += 1

                    # Store author and timestamp for each modification
                    dictfiles[filename]['history'].append({'author': author, 'date': date})

                    # [Optimization 5] Log filename and modification details for debugging
                    print(f"File: {filename} | Author: {author} | Date: {date}")

            ipage += 1  # Move to the next page of commits

    except Exception as e:
        # [Optimization 6] Capture and print specific errors for better debugging
        print(f"Error receiving data: {e}")
        exit(0)  # Exit on error to prevent infinite looping
