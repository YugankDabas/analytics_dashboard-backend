from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.user import User
from app.core.security import decode_token
from fastapi.security import HTTPBearer

security = HTTPBearer()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
    credentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    token = credentials.credentials
    username = decode_token(token)

    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )

    user = db.query(User).filter(User.username == username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user