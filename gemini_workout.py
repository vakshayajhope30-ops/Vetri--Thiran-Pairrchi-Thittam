from app.ai.gemini_client import generate_text
from app.config import settings

def generate_workout(name: str, age: int, weight: float, goal: str, intensity: str) -> str:
    prompt = f"""
You are FitBuddy AI, a fitness planning assistant.

Create a personalized 7-day workout plan.

Name: {name}
Age: {age}
Weight: {weight} kg
Fitness Goal: {goal}
Workout Intensity: {intensity}

Requirements:
- Create exactly 7 days.
- Clearly label Day 1 through Day 7.
- Include warm-up for active days.
- Include main exercises with sets/reps or duration.
- Include rest intervals.
- Include cooldown or recovery guidance.
- Include rest/recovery days where appropriate.
- Match the requested intensity.
- Make it practical for a general adult.
- Do not prescribe medication or supplements.
- Do not claim it replaces professional medical advice.
- Keep the output easy to follow.

Format:
FITBUDDY 7-DAY WORKOUT PLAN

Day 1 - Focus
Warm-up:
- ...
Main Workout:
- Exercise — sets x reps
Rest:
- ...
Cooldown:
- ...

Repeat through Day 7.

GENERAL SAFETY NOTES:
- Start gradually.
- Stop if you experience unusual pain, dizziness, chest pain, or difficulty breathing.
- Consult a qualified healthcare professional for medical conditions or concerns.
"""
    return generate_text(prompt, settings.GEMINI_WORKOUT_MODEL, 0.7, 7000)
