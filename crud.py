from sqlalchemy.orm import Session
from app.models import User

def get_user_by_user_id(db: Session, user_id: str):
    return db.query(User).filter(User.user_id == user_id).first()

def get_all_users(db: Session):
    return db.query(User).order_by(User.created_at.desc()).all()

def create_user(db, user_id, name, age, weight, goal, intensity, original_plan, nutrition_tip):
    user = User(
        user_id=user_id, name=name, age=age, weight=weight,
        goal=goal, intensity=intensity,
        original_plan=original_plan, nutrition_tip=nutrition_tip
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def update_user_plan(db, user, updated_plan, feedback):
    user.updated_plan = updated_plan
    user.feedback = feedback
    db.commit()
    db.refresh(user)
    return user
