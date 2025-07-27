import os
import httpx
from core.config import settings

OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}


def generate_response_openrouter(prompt: str, system_prompt: str = "You are a helpful AI assistant.") -> str:
    payload = {
        "model": settings.OPENROUTER_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    try:
        response = httpx.post(OPENROUTER_API_URL, json=payload, headers=HEADERS)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()

    except httpx.RequestError as e:
        print(f"HTTP Request failed: {e}")
        return "OpenRouter API request failed."
    except Exception as e:
        print(f"Unexpected error: {e}")
        return "Unexpected error during LLM response generation."
