from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import UserCreate
from app.services import user_service

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserCreate, status_code=201)
def create_user(user: UserCreate, db = Depends(get_db)):
    return user_service.add_user(user, db)


@router.get("/", response_model=list[UserCreate])
def get_users(db = Depends(get_db)):
    return user_service.get_all_users(db)

@router.get("/{email}", response_model = UserCreate)
def get_user_by_email(email: str, db = Depends(get_db)):
    return user_service.get_user_by_email(email, db)


@router.get("/{user_id}", response_model=UserCreate)
def get_user(user_id: int, db = Depends(get_db)):
    return user_service.get_user_by_id(user_id, db)