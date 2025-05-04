import requests
from pandas import DataFrame

def search_github_repos(token, query, language="", stars="20", license_type=""):
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }

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
