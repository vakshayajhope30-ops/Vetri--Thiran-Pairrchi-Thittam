import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_NAME = os.getenv("APP_NAME", "FitBuddy AI")
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
    GEMINI_WORKOUT_MODEL = os.getenv("GEMINI_WORKOUT_MODEL", "gemini-2.5-pro")
    GEMINI_TIP_MODEL = os.getenv("GEMINI_TIP_MODEL", "gemini-2.5-flash")
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./fitbuddy.db")

settings = Settings()
