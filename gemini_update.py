from app.ai.gemini_client import generate_text
from app.config import settings

def update_workout_plan(original_plan: str, feedback: str, name: str, goal: str, intensity: str) -> str:
    prompt = f"""
You are FitBuddy AI.

A user wants an existing 7-day workout plan revised.

Name: {name}
Goal: {goal}
Intensity: {intensity}

ORIGINAL PLAN:
{original_plan}

USER FEEDBACK:
{feedback}

Create a revised 7-day plan.

Rules:
- Preserve useful parts of the original.
- Apply reasonable feedback.
- Keep exactly 7 days.
- Match the requested intensity.
- Include warm-up, main workout, rest/recovery and cooldown where appropriate.
- Include sets/reps or duration.
- Avoid unsafe extreme training.
- Do not prescribe medication or supplements.

Use:
UPDATED FITBUDDY 7-DAY WORKOUT PLAN

Day 1 - ...
Day 2 - ...
Day 3 - ...
Day 4 - ...
Day 5 - ...
Day 6 - ...
Day 7 - ...

UPDATED SAFETY NOTES:
...
"""
    return generate_text(prompt, settings.GEMINI_WORKOUT_MODEL, 0.7, 7000)
