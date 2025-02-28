import csv

def getAuthorDate(filesList, lsttokens, repo):
    """
    Fetches commit information (filename, author, and date) from a GitHub repository.

    Args:
        filesList (list): A list to store commit information tuples (filename, author, date).
        lsttokens (list): A list of GitHub authentication tokens.
        repo (str): The GitHub repository in the format "owner/repository".

    Returns:
        None: The function appends commit information directly to `filesList`.
    """
    page_num = 1  # Counter for paginated API requests
    token_index = 0  # Counter to cycle through authentication tokens

    try:
        # Loop through commit history pages until an empty response is received
        while True:
            commits_url = f'https://api.github.com/repos/{repo}/commits?page={page_num}&per_page=100'
            jsonCommits, token_index = github_auth(commits_url, lsttokens, token_index)

            # Exit loop if no commits are returned
            if not jsonCommits:
                break

            # Process each commit in the retrieved page
            for shaObject in jsonCommits:
                sha = shaObject['sha']

                # Fetch commit details using the commit SHA
                sha_url = f'https://api.github.com/repos/{repo}/commits/{sha}'
                shaDetails, token_index = github_auth(sha_url, lsttokens, token_index)

                # Extract commit details
                commit_data = shaDetails.get('commit', {})
                filesjson = shaDetails.get('files', [])

                # Get author name and commit date
                author = commit_data.get('author', {}).get('name', 'Unknown')
                date = commit_data.get('author', {}).get('date', 'Unknown')

                # Extract source file names from the commit
                files = [
                    file_info['filename']
                    for file_info in filesjson
                    if 'src' in file_info['filename']
                ]

                # Store commit info in the list
                for file in files:
                    filesList.append((file, author, date))

            page_num += 1  # Move to the next page of commits

    except Exception as e:
        print(f"Error receiving data: {e}")
        exit(1)

# GitHub repository information
repo = 'scottyab/rootbeer'

# List of GitHub API authentication tokens (cycle through these to avoid rate limits)
lstTokens = ["YOUR_GITHUB_TOKEN_HERE"]  # Replace with actual token

# Initialize the list to store commit information
filesList = []

# Fetch commit information
getAuthorDate(filesList, lstTokens, repo)

# Output file path
fileOutput = 'data/file_authorDate.csv'

# Write commit data to CSV file
with open(fileOutput, 'w', newline='') as fileCSV:
    writer = csv.writer(fileCSV)
    
    # Write header row
    writer.writerow(["Filename", "Author", "Date"])

    # Write commit details
    writer.writerows(filesList)

print(f"Commit data successfully written to {fileOutput}")