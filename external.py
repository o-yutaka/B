from typing import List

import requests


def fetch_github_trending_topics(limit: int = 5) -> List[str]:
    try:
        url = "https://api.github.com/search/repositories"
        params = {"q": "stars:>1000 pushed:>2024-01-01", "sort": "stars", "order": "desc", "per_page": limit}
        res = requests.get(url, params=params, timeout=20)
        res.raise_for_status()
        data = res.json()
        return [item.get("full_name", "") for item in data.get("items", []) if item.get("full_name")]
    except Exception:
        return []


def generate_external_tasks() -> List[str]:
    trends = fetch_github_trending_topics(5)
    tasks = []
    for name in trends:
        tasks.append(f"Analyze popular problem patterns from repository {name} and propose a mini product")
    return tasks
