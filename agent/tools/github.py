import requests

def fetch_pr_diff(repo_url, pr_number):
    api_url = repo_url.replace("https://github.com", "https://api.github.com/repos")
    diff_url = f"{api_url}/pulls/{pr_number}"
    headers = {"Accept": "application/vnd.github.v3.diff"}
    response = requests.get(diff_url, headers=headers)
    response.raise_for_status()
    return response.text