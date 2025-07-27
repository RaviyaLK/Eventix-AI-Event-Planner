from langgraph.graph import StateGraph, END
from agents.search_agent import search_agent
from agents.planner_agent import planner_agent
from agents.budget_agent import budget_agent
from agents.report_agent import report_agent
from langgraph_flow.state import PlannerState

def build_event_planner_graph():
    graph = StateGraph(PlannerState)  # Pass the schema here

    graph.add_node("search", lambda state: {"context": search_agent(state["task"])})
    graph.add_node("planner", lambda state: {"agenda": planner_agent(state["context"])})
    graph.add_node("budget", lambda state: {"budget": budget_agent(state["agenda"])})
    graph.add_node("report", lambda state: {"report": report_agent(state["budget"], state["agenda"])})

    graph.set_entry_point("search")
    graph.add_edge("search", "planner")
    graph.add_edge("planner", "budget")
    graph.add_edge("budget", "report")
    graph.add_edge("report", END)

    return graph.compile()
