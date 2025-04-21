import requests
import pandas as pd
from tkinter import messagebox
from config import get_github_token

def search_github_repos(query, sort="stars", order="desc", per_page=30, max_pages=3):
    token = get_github_token()
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {token}"
    }

    all_repos = []
    for page in range(1, max_pages + 1):
        url = f"https://api.github.com/search/repositories?q={query}&sort={sort}&order={order}&per_page={per_page}&page={page}"
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            messagebox.showerror("Error", f"GitHub API Error: {response.status_code}")
            return pd.DataFrame()
        items = response.json().get("items", [])
        for repo in items:
            all_repos.append({
                "Name": repo["full_name"],
                "Stars": repo["stargazers_count"],
                "Language": repo["language"],
                "Description": repo["description"],
                "URL": repo["html_url"],
                "Last Updated": repo["updated_at"]
            })
    return pd.DataFrame(all_repos)
