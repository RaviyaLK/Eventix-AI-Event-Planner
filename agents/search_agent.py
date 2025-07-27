import re
from typing import Tuple, Dict, Any
from tools.web_search import tavily_search
import logging

logger = logging.getLogger(__name__)

known_locations = [
    "Sri Lanka", "Japan", "Colombo", "Tokyo", "USA",
    "New York", "India", "Germany", "Berlin", "France", "Paris"
]

def extract_location_and_topic(prompt: str) -> Tuple[str, str]:
    """
    Extract event topic and location from prompt using simple heuristics.

    Args:
        prompt (str): User input prompt.

    Returns:
        Tuple[str, str]: (topic, location) extracted from prompt.
    """
    lower_prompt = prompt.lower()
    location = next((loc for loc in known_locations if loc.lower() in lower_prompt), "your location")

    match = re.search(
        r"(?:plan|organize|host|create).+?(conference|summit|meetup|hackathon|event|workshop)(?: on| about)? (.+?) (?:in|at|near) ([\w\s]+)",
        prompt, re.IGNORECASE
    )

    if match:
        topic = match.group(2).strip()
        
        loc_from_regex = match.group(3).strip()
        location = loc_from_regex if loc_from_regex else location
    else:
       
        fallback_match = re.search(
            r"(?:plan|organize|host|create).+?(conference|summit|meetup|hackathon|event|workshop)(?: on| about)? (.+)", prompt, re.IGNORECASE
        )
        topic = fallback_match.group(2).strip() if fallback_match else "technology"

    return topic, location


def search_agent(prompt: str) -> Dict[str, Any]:
    """
    Perform a venue and vendor search based on extracted topic and location.

    Args:
        prompt (str): User's event description.

    Returns:
        dict: Search results including venue suggestions and query used.
    """
    topic, location = extract_location_and_topic(prompt)
    query = f"venues for {topic} conference in {location}"

    logger.debug(f"Search query: {query}")

    try:
        results = tavily_search(query, max_results=5)
        logger.debug(f"Search results count: {len(results)}")
    except Exception as e:
        logger.error(f"Error during tavily_search: {e}")
        results = []

    suggestions = []
    for result in results:
        snippet = " ".join(result.split()) 
        name = snippet[:60] + "..." if len(snippet) > 60 else snippet
        estimated_cost = "USD 1,000–5,000"  
        suggestions.append({
            "name": name,
            "description": snippet,
            "estimated_cost": estimated_cost
        })
        if len(suggestions) >= 3:
            break

    return {"agent": "SearchAgent", "venues": suggestions, "query_used": query}
