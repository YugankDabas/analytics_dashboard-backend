from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.feature_click import (
    FeatureClickCreate,
    FeatureClickResponse,
)
from app.services.feature_click_service import create_feature_click
from app.core.dependencies import get_db, get_current_user
from app.models.user import User

router = APIRouter(prefix="/track", tags=["tracking"])


@router.post("/", response_model=FeatureClickResponse)
def track_feature(
    payload: FeatureClickCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    feature_click = create_feature_click(
        db=db,
        user=current_user,
        feature_name=payload.feature_name,
    )

    return feature_click