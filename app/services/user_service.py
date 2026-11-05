from fastapi import HTTPException, status, Depends
from app.database import get_db
from sqlalchemy.orm import Session
from app.models.ORM_models import UserDB
from app.models.user import UserCreate


def add_user(data: UserCreate, db = Depends(get_db)):
    if db.query(UserDB).filter(UserDB.id == data.id).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User ID already exists")
    user = UserDB(**data.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_id(user_id: int, db = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

def get_user_by_email(email: str, db = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.email == email).first()
    if not user:
        raise HTTPException(status_code = 401, detail = "Invalid email or password")
    return user

def get_all_users(db = Depends(get_db)):
    return db.query(UserDB).all()