# agents/budget_agent.py

from tools.llm_router import call_openrouter


def budget_agent(state: dict) -> dict:
    task = state.get("task", "")
    search_data = state.get("search_agent_response", "")
    budget_limit = state.get("budget_limit", None)

    budget_instruction = (
        f"The user has a budget limit of ${budget_limit}. "
        f"Ensure all cost estimations fit within this budget. "
        f"If you exceed it, clearly state it and suggest compromises."
        if budget_limit else
        "There is no fixed budget. You can estimate a reasonable mid-tier budget."
    )

    prompt = f"""
You are a financial planner for events.

{budget_instruction}

Based on the following event request and available search data (venues, vendors, etc.), prepare a **realistic budget breakdown**:

---

**Event Description:**
{task}

---

**Available Data (Venues, Vendors):**
{search_data}

Include:
- Venue cost
- Catering
- Speaker fees
- Equipment
- Marketing
- Miscellaneous

Output in table format and give a final total.
Mention if the plan exceeds the user's budget.
"""

    budget = call_openrouter(prompt)

    return {
        "agent": "BudgetAgent",
        "budget_breakdown": budget
    }
