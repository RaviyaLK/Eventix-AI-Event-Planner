from langchain_core.prompts import PromptTemplate
from tools.llm_router import call_openrouter

report_prompt = PromptTemplate.from_template(
    "Write a structured event report based on the following agenda and budget:\n\nAgenda:\n{agenda}\n\nBudget:\n{budget}\n\nInclude Introduction, Objectives, Key Points, Conclusion."
)

def report_agent(budget: str, agenda: str) -> str:
    prompt = report_prompt.format(budget=budget, agenda=agenda)
    return call_openrouter(prompt)
