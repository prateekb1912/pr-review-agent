import requests

def fetch_pr_diff(repo_url, pr_number):
    api_url = repo_url.replace("https://github.com", "https://api.github.com/repos")
    pr_url = f"{api_url}/pulls/{pr_number}"
    headers = {"Accept": "application/vnd.github.v3+json"}
    response = requests.get(pr_url, headers=headers)
    response.raise_for_status()

    pr_data = response.json()
    diff_url = pr_data["diff_url"]
    pr_title = pr_data["title"]
    pr_description = pr_data["body"]

    diff_response = requests.get(diff_url, headers=headers)
    diff_response.raise_for_status()

    return diff_response.text, pr_title, pr_description