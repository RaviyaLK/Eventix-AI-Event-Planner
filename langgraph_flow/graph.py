from langgraph.graph import StateGraph, END
from agents.search_agent import search_agent
from agents.planner_agent import planner_agent
from agents.budget_agent import budget_agent
from agents.report_agent import report_agent
from langgraph_flow.state import PlannerState
import re

def extract_budget(text: str) -> int | None:
    # Very basic regex for now, can be improved later
    match = re.search(r"\$?(\d{1,3}(?:,\d{3})+|\d+)\s*(usd|dollars)?", text.lower())
    if match:
        amount_str = match.group(1).replace(",", "")
        return int(amount_str)
    return None

def build_event_planner_graph():
    graph = StateGraph(PlannerState)  # Pass the schema here

    # Entry node: add budget_limit to state
    def start_node(state):
        state["budget_limit"] = extract_budget(state.get("task", ""))
        return {}

    graph.add_node("start", start_node)

    # Search node uses 'task' and outputs 'search_agent_response'
    def search_node(state):
        search_results = search_agent(state["task"])
        return {"search_agent_response": search_results}

    graph.add_node("search", search_node)

    # Budget node uses task, search_agent_response, budget_limit, outputs budget_breakdown
    def budget_node(state):
        budget = budget_agent({
            "task": state["task"],
            "search_agent_response": state.get("search_agent_response", ""),
            "budget_limit": state.get("budget_limit"),
        })
        return {"budget_breakdown": budget["budget_breakdown"]}

    graph.add_node("budget", budget_node)

    # Planner node uses task, search_agent_response, budget_breakdown, budget_limit; outputs final_plan
    def planner_node(state):
        plan = planner_agent({
            "task": state["task"],
            "search_agent_response": state.get("search_agent_response", ""),
            "budget_breakdown": state.get("budget_breakdown", ""),
            "budget_limit": state.get("budget_limit"),
        })
        return {"final_plan": plan["final_plan"]}

    graph.add_node("planner", planner_node)

    # Report node uses all relevant info, outputs report
    def report_node(state):
        report = report_agent({
            "task": state["task"],
            "search_agent_response": state.get("search_agent_response", ""),
            "budget_breakdown": state.get("budget_breakdown", ""),
            "final_plan": state.get("final_plan", ""),
            "budget_limit": state.get("budget_limit"),
        })
        return {"report": report["report"]}

    graph.add_node("report", report_node)

    # Flow: start -> search -> budget -> planner -> report -> END
    graph.set_entry_point("start")
    graph.add_edge("start", "search")
    graph.add_edge("search", "budget")
    graph.add_edge("budget", "planner")
    graph.add_edge("planner", "report")
    graph.add_edge("report", END)

    return graph.compile()
