
import requests
from core.config import settings

def tavily_search(query: str, max_results: int = 5) -> list:
    api_key = settings.TAVILY_API_KEY
    response = requests.get(
        "https://api.tavily.com/search",
        params={"query": query, "num_results": max_results},
        headers={"Authorization": f"Bearer {api_key}"}
    )
    data = response.json()
    return [item["content"] for item in data.get("results", [])]
