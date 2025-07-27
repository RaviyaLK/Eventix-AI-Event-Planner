# agents/budget_agent.py

from langchain_core.prompts import PromptTemplate
from tools.llm_router import call_openrouter

budget_prompt = PromptTemplate.from_template(
    "Estimate a budget breakdown (venue, food, tech, logistics) for the following:\n{agenda}\n\nReturn itemized costs."
)

def budget_agent(agenda: str) -> str:
    prompt = budget_prompt.format(agenda=agenda)
    return call_openrouter(prompt)
