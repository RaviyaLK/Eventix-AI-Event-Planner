

from langchain_core.prompts import PromptTemplate
from tools.llm_router import call_openrouter

prompt_template = PromptTemplate.from_template(
    "You're a professional event planner. Given the context:\n{context}\n\nPlan a 2-day tech conference agenda."
)

def planner_agent(context: str) -> str:
    prompt = prompt_template.format(context=context)
    return call_openrouter(prompt)
