import requests
<<<<<<< HEAD
from pandas import DataFrame

def search_github_repos(token, query, language="", stars="20", license_type=""):
=======
import pandas as pd

def search_github_repos(token, query, language_filter="", stars_filter="0", sort="stars", order="desc", per_page=30, max_pages=3):
>>>>>>> 67d32e25915453c87537ab1f1af2714db8b4588e
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    full_query = f"{query} stars:>{stars_filter}"
    if language_filter:
        full_query += f" language:{language_filter}"

<<<<<<< HEAD
    # ✅ Dynamically build query parts
    query_parts = [query]
    if language:
        query_parts.append(f"language:{language}")
    if stars:
        query_parts.append(f"stars:>={stars}")
    if license_type:
        query_parts.append(f"license:{license_type}")

    full_query = " ".join(query_parts)

    params = {
        "q": full_query,
        "sort": "stars",
        "order": "desc",
        "per_page": 30
    }

    print(f"[DEBUG] Querying GitHub API with: {params['q']}")

    response = requests.get("https://api.github.com/search/repositories", headers=headers, params=params)

    print(f"[DEBUG] Status: {response.status_code}")
    print(f"[DEBUG] Response: {response.text[:500]}")

    if response.status_code != 200:
        try:
            message = response.json().get('message')
            raise Exception(f"{response.status_code}: {message}")
        except Exception:
            raise Exception(f"{response.status_code}: API request failed.")

    items = response.json().get("items", [])
    data = [{
        "Name": repo["full_name"],
        "Stars": repo["stargazers_count"],
        "Language": repo["language"],
        "License": repo["license"]["spdx_id"] if repo["license"] else "None",
        "URL": repo["html_url"]
    } for repo in items]

    return DataFrame(data)
=======
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
>>>>>>> 67d32e25915453c87537ab1f1af2714db8b4588e
