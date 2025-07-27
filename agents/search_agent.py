# agents/search_agent.py

from tools.web_search import tavily_search

def search_agent(task: str) -> str:
    results = tavily_search(task)
    return "\n".join(results)
