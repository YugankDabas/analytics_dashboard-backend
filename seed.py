import random
from datetime import datetime, timedelta

from faker import Faker
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.db.init_db import init_db
from app.models.user import User
from app.models.feature_click import FeatureClick
from app.core.security import hash_password

fake = Faker()


FEATURES = [
    "filter_change",
    "bar_chart_click",
    "line_chart_click",
    "date_range_update",
    "gender_filter",
    "age_filter",
]


def create_users(db: Session, count: int = 10):
    users = []

    for _ in range(count):
        user = User(
            username=fake.unique.user_name(),
            hashed_password=hash_password("password123"),
            age=random.randint(15, 60),
            gender=random.choice(["male", "female", "other"]),
        )
        db.add(user)
        users.append(user)

    db.commit()

    for user in users:
        db.refresh(user)

    return users


def create_feature_clicks(
    db: Session,
    users: list[User],
    min_clicks: int = 100,
    max_clicks: int = 200,
):
    total_clicks = random.randint(min_clicks, max_clicks)

    clicks = []

    for _ in range(total_clicks):
        random_user = random.choice(users)

        random_days_ago = random.randint(0, 30)
        random_time = datetime.utcnow() - timedelta(
            days=random_days_ago,
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59),
        )

        click = FeatureClick(
            user_id=random_user.id,
            feature_name=random.choice(FEATURES),
            timestamp=random_time,
        )

        clicks.append(click)

    db.bulk_save_objects(clicks)
    db.commit()

    return total_clicks


def main():
    print("Initializing database...")
    init_db()

    db = SessionLocal()

    try:
        print("Seeding users...")
        users = create_users(db, count=10)

        print("Seeding feature clicks...")
        total_clicks = create_feature_clicks(db, users)

        print("Seed completed successfully.")
        print(f"Created {len(users)} users")
        print(f"Created {total_clicks} feature clicks")

    finally:
        db.close()


if __name__ == "__main__":
    main()