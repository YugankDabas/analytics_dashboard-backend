from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, get_current_user
from app.models.user import User
from app.services.analytics_service import get_analytics_data

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/")
def analytics(
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    age_group: Optional[str] = Query(None),
    gender: Optional[str] = Query(None),
    feature_name: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_analytics_data(
        db=db,
        start_date=start_date,
        end_date=end_date,
        age_group=age_group,
        gender=gender,
        feature_name=feature_name,
    )