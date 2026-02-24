from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import timedelta

from app.schemas.user import UserCreate, UserLogin, Token
from app.services.auth_service import register_user, authenticate_user
from app.core.security import create_access_token
from app.core.dependencies import get_db
from app.core.config import get_settings

settings = get_settings()

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=Token)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    user = register_user(db, user_data)

    access_token = create_access_token(
        subject=user.username,
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    return Token(access_token=access_token)


@router.post("/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, user_data.username, user_data.password)

    access_token = create_access_token(
        subject=user.username,
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    return Token(access_token=access_token)