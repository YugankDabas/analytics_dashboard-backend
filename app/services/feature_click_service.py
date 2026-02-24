from sqlalchemy.orm import Session

from app.models.feature_click import FeatureClick
from app.models.user import User


def create_feature_click(
    db: Session,
    user: User,
    feature_name: str,
) -> FeatureClick:
    feature_click = FeatureClick(
        user_id=user.id,
        feature_name=feature_name,
    )

    db.add(feature_click)
    db.commit()
    db.refresh(feature_click)

    return feature_click