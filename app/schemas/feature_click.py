from datetime import datetime
from pydantic import BaseModel


class FeatureClickCreate(BaseModel):
    feature_name: str


class FeatureClickResponse(BaseModel):
    id: int
    feature_name: str
    timestamp: datetime

    class Config:
        from_attributes = True