
from tools.llm_router import call_openrouter


def report_agent(state: dict) -> dict:
    task = state.get("task", "")
    search_data = state.get("search_agent_response", "")
    budget_data = state.get("budget_breakdown", "")
    planner_output = state.get("final_plan", "")

    prompt = f"""
You are a senior technical report writer and project planner assistant.

Based on the following data, generate a professional and structured **Event Planning Report**.

---

**Event Request:**
{task}

---

**Search Results (Venues, Speakers, Vendors):**
{search_data}

---

**Budget Breakdown:**
{budget_data}

---

**Event Plan and Agenda:**
{planner_output}

---

📝 Your job:
- Organize the report with proper section headings (like Executive Summary, Venue Options, Agenda, Budget, Recommendations).
- Ensure everything is clearly formatted and easy to read.
- Summarize where needed but preserve important details.
- Close with a short “Next Steps” section for the client.

Keep the tone professional, clear, and useful for decision-making.
"""

    report = call_openrouter(prompt)

    return {
        "agent": "ReportAgent",
        "report": report
    }
