from pydantic import BaseModel, Field, field_validator

class UserInput(BaseModel):
    user_id: str = Field(..., min_length=2, max_length=100)
    name: str = Field(..., min_length=2, max_length=100)
    age: int = Field(..., ge=13, le=100)
    weight: float = Field(..., gt=20, le=300)
    goal: str = Field(..., min_length=2, max_length=100)
    intensity: str = Field(..., min_length=2, max_length=20)

    @field_validator("name", "user_id", "goal", "intensity")
    @classmethod
    def strip_values(cls, value: str) -> str:
        return value.strip()

class FeedbackRequest(BaseModel):
    user_id: str = Field(..., min_length=2, max_length=100)
    feedback: str = Field(..., min_length=3, max_length=2000)

    @field_validator("user_id", "feedback")
    @classmethod
    def strip_values(cls, value: str) -> str:
        return value.strip()
