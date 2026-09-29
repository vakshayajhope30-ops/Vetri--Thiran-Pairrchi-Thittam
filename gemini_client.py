from functools import lru_cache
from google import genai
from app.config import settings

@lru_cache(maxsize=1)
def get_gemini_client():
    if not settings.GOOGLE_API_KEY:
        raise RuntimeError("GOOGLE_API_KEY is missing. Add it to the .env file.")
    return genai.Client(api_key=settings.GOOGLE_API_KEY)

def generate_text(prompt: str, model: str, temperature: float = 0.7, max_output_tokens: int = 5000) -> str:
    client = get_gemini_client()
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config={
            "temperature": temperature,
            "max_output_tokens": max_output_tokens,
        },
    )
    if not response.text:
        raise RuntimeError("Gemini returned an empty response.")
    return response.text.strip()
