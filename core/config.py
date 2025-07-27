import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY")
    OPENROUTER_MODEL: str = "deepseek/deepseek-chat-v3-0324:free"
    TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY")

settings = Settings()
