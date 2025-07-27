from typing import TypedDict

class PlannerState(TypedDict):
    task: str
    context: str
    agenda: str
    budget: str
    report: str
