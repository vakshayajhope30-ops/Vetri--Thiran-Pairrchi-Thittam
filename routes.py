from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.ai.gemini_nutrition import generate_nutrition_tip
from app.ai.gemini_update import update_workout_plan
from app.ai.gemini_workout import generate_workout
from app.crud import create_user, get_all_users, get_user_by_user_id, update_user_plan
from app.database import get_db
from app.schemas import FeedbackRequest, UserInput

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={"error": None})

@router.post("/generate-workout", response_class=HTMLResponse)
def generate_workout_route(
    request: Request,
    user_id: str = Form(...),
    name: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),
    db: Session = Depends(get_db),
):
    try:
        user_input = UserInput(
            user_id=user_id, name=name, age=age, weight=weight,
            goal=goal, intensity=intensity
        )

        if get_user_by_user_id(db, user_input.user_id):
            return templates.TemplateResponse(
                request=request,
                name="index.html",
                context={"error": "This User ID already exists. Please use a different User ID."},
                status_code=400,
            )

        workout_plan = generate_workout(
            user_input.name, user_input.age, user_input.weight,
            user_input.goal, user_input.intensity
        )
        nutrition_tip = generate_nutrition_tip(user_input.goal)

        user = create_user(
            db=db,
            user_id=user_input.user_id,
            name=user_input.name,
            age=user_input.age,
            weight=user_input.weight,
            goal=user_input.goal,
            intensity=user_input.intensity,
            original_plan=workout_plan,
            nutrition_tip=nutrition_tip,
        )

        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "user": user,
                "workout_plan": workout_plan,
                "nutrition_tip": nutrition_tip,
                "updated": False,
                "message": "Your personalized plan has been generated!",
                "error": None,
            },
        )

    except Exception as exc:
        print(f"Generation error: {exc}")
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={"error": "Unable to generate the plan. Check your Gemini API key and try again."},
            status_code=500,
        )

@router.post("/submit-feedback", response_class=HTMLResponse)
def submit_feedback(
    request: Request,
    user_id: str = Form(...),
    feedback: str = Form(...),
    db: Session = Depends(get_db),
):
    user = get_user_by_user_id(db, user_id)

    if not user:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={"error": "User ID was not found. Please check your User ID."},
            status_code=404,
        )

    try:
        feedback_request = FeedbackRequest(user_id=user_id, feedback=feedback)

        updated_plan = update_workout_plan(
            original_plan=user.original_plan,
            feedback=feedback_request.feedback,
            name=user.name,
            goal=user.goal,
            intensity=user.intensity,
        )

        user = update_user_plan(
            db, user, updated_plan, feedback_request.feedback
        )

        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "user": user,
                "workout_plan": updated_plan,
                "nutrition_tip": user.nutrition_tip,
                "updated": True,
                "message": "Your workout plan was successfully updated!",
                "error": None,
            },
        )

    except Exception as exc:
        print(f"Update error: {exc}")
        return templates.TemplateResponse(
            request=request,
            name="result.html",
            context={
                "user": user,
                "workout_plan": user.updated_plan or user.original_plan,
                "nutrition_tip": user.nutrition_tip,
                "updated": False,
                "message": None,
                "error": "Unable to update the plan. Check your Gemini API key and try again.",
            },
            status_code=500,
        )

@router.get("/view-all-users", response_class=HTMLResponse)
def view_all_users(request: Request, db: Session = Depends(get_db)):
    users = get_all_users(db)
    return templates.TemplateResponse(
        request=request,
        name="all_users.html",
        context={"users": users},
    )

@router.get("/health")
def health_check():
    return {"status": "healthy", "application": "FitBuddy AI"}
