from tools.llm_router import call_openrouter

def planner_agent(state: dict) -> dict:
    """
    Generate a detailed event plan including venue, agenda, and speaker suggestions
    based on the user's task, search results, and budget data.

    Args:
        state (dict): A dictionary containing:
            - task (str): The user's event description.
            - search_agent_response (dict): Search results from the search agent.
            - budget_breakdown (str): Budget details from the budget agent.
            - budget_limit (int, optional): User's budget limit, if any.

    Returns:
        dict: Contains 'agent' name and 'final_plan' as the event plan string.
    """

    task = state.get("task", "")
    search_data = state.get("search_agent_response", {})
    budget_data = state.get("budget_breakdown", "")
    budget_limit = state.get("budget_limit", None)

    if not task:
        return {
            "agent": "PlannerAgent",
            "final_plan": "Missing event description from the user."
        }

    prompt = f"""
You are a highly skilled professional event planner.

Given this event request from a client:
\"\"\"{task}\"\"\"

Based on these real-world suggestions and options from the web search:
{search_data}

Here is the estimated budget breakdown:
{budget_data}

The user's budget limit is: {budget_limit if budget_limit else 'No fixed budget'}

Your tasks:
1. Propose the best suitable venue from the above suggestions.
2. Suggest relevant and appropriate guest speakers or partners.
3. Create a realistic and detailed event agenda — break it down by time blocks (e.g., 9:00 AM - 10:00 AM: Registration).
4. Make sure everything fits within the given budget limit (if provided).
5. Keep the tone professional and clear, suitable for a formal proposal.

Please provide a well-structured event plan covering venue, agenda, and speaker suggestions.
"""

    plan = call_openrouter(prompt)

    return {
        "agent": "PlannerAgent",
        "final_plan": plan
    }
