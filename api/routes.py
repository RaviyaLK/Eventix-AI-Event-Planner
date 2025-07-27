from fastapi import APIRouter
from pydantic import BaseModel
from langgraph_flow.graph import build_event_planner_graph

router = APIRouter()

class EventRequest(BaseModel):
    prompt: str

@router.post("/plan/")
async def plan_event(request: EventRequest):
    planner_graph = build_event_planner_graph()
    result = planner_graph.invoke({"task": request.prompt})
    return {"report": result["report"]}
