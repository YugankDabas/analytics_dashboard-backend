from datetime import datetime

from sqlalchemy import String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class FeatureClick(Base):
    __tablename__ = "feature_clicks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    feature_name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)

    timestamp: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True,
    )

    user = relationship("User", backref="feature_clicks")