from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password, verify_password


def register_user(db: Session, user_data: UserCreate) -> User:
    existing_user = db.query(User).filter(User.username == user_data.username).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    new_user = User(
        username=user_data.username,
        hashed_password=hash_password(user_data.password),
        age=user_data.age,
        gender=user_data.gender,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

def authenticate_user(db: Session, username: str, password: str) -> User:
    user = db.query(User).filter(User.username == username).first()

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    return user