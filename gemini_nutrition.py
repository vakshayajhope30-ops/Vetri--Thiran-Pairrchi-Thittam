from app.ai.gemini_client import generate_text
from app.config import settings

def generate_nutrition_tip(goal: str) -> str:
    prompt = f"""
You are FitBuddy AI's nutrition and recovery assistant.

Fitness goal: {goal}

Provide one concise, practical nutrition or recovery tip.

Requirements:
- 80 to 150 words.
- Easy to understand.
- General healthy eating and recovery guidance.
- No medication or dangerous calorie restrictions.
- No guaranteed medical or weight-loss outcomes.
- Mention hydration or balanced nutrition when relevant.
- Return only the tip.
"""
    return generate_text(prompt, settings.GEMINI_TIP_MODEL, 0.5, 500)
