import requests
import pandas as pd

def search_github_repos(token, query, language_filter="", stars_filter="0", sort="stars", order="desc", per_page=30, max_pages=3):
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {token}"
    }
    full_query = f"{query} stars:>{stars_filter}"
    if language_filter:
        full_query += f" language:{language_filter}"

    all_repos = []
    for page in range(1, max_pages + 1):
        url = f"https://api.github.com/search/repositories?q={full_query}&sort={sort}&order={order}&per_page={per_page}&page={page}"
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception(f"GitHub API Error: {response.status_code}\n{response.text}")
        for repo in response.json().get("items", []):
            all_repos.append({
                "Name": repo["full_name"],
                "Stars": repo["stargazers_count"],
                "Language": repo["language"],
                "Description": repo["description"],
                "URL": repo["html_url"],
                "Last Updated": repo["updated_at"]
            })
    return pd.DataFrame(all_repos)
