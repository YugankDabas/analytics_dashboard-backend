from datetime import datetime
from typing import Optional, List, Dict

from sqlalchemy import func, and_
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.feature_click import FeatureClick


def _apply_filters(
    query,
    start_date: Optional[datetime],
    end_date: Optional[datetime],
    age_group: Optional[str],
    gender: Optional[str],
):
    conditions = []

    if start_date:
        conditions.append(FeatureClick.timestamp >= start_date)

    if end_date:
        conditions.append(FeatureClick.timestamp <= end_date)

    if age_group:
        if age_group == "<18":
            conditions.append(User.age < 18)
        elif age_group == "18-40":
            conditions.append(and_(User.age >= 18, User.age <= 40))
        elif age_group == ">40":
            conditions.append(User.age > 40)

    if gender:
        conditions.append(User.gender == gender)

    if conditions:
        query = query.filter(and_(*conditions))

    return query


def get_analytics_data(
    db: Session,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    age_group: Optional[str] = None,
    gender: Optional[str] = None,
    feature_name: Optional[str] = None,
) -> Dict[str, List[Dict]]:
    bar_query = (
        db.query(
            FeatureClick.feature_name.label("feature_name"),
            func.count(FeatureClick.id).label("total_clicks"),
        )
        .join(User, FeatureClick.user_id == User.id)
    )

    bar_query = _apply_filters(
        bar_query, start_date, end_date, age_group, gender
    )

    bar_results = (
        bar_query
        .group_by(FeatureClick.feature_name)
        .order_by(func.count(FeatureClick.id).desc())
        .all()
    )

    bar_chart = [
        {
            "feature_name": row.feature_name,
            "total_clicks": row.total_clicks,
        }
        for row in bar_results
    ]

    line_chart = []

    if feature_name:
        line_query = (
            db.query(
                func.date_trunc("day", FeatureClick.timestamp).label("date"),
                func.count(FeatureClick.id).label("clicks"),
            )
            .join(User, FeatureClick.user_id == User.id)
            .filter(FeatureClick.feature_name == feature_name)
        )

        line_query = _apply_filters(
            line_query, start_date, end_date, age_group, gender
        )

        line_results = (
            line_query
            .group_by(func.date_trunc("day", FeatureClick.timestamp))
            .order_by(func.date_trunc("day", FeatureClick.timestamp))
            .all()
        )

        line_chart = [
            {
                "date": row.date.date().isoformat(),
                "clicks": row.clicks,
            }
            for row in line_results
        ]

    return {
        "bar_chart": bar_chart,
        "line_chart": line_chart,
    }