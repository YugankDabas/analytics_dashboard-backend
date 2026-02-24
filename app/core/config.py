from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings
from sqlalchemy.engine import URL


class Settings(BaseSettings):
    PROJECT_NAME: str = "Interactive Product Analytics Dashboard"

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str
    DATABASE_URL: str | None = None

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:5173"]

    @property
    def SQLALCHEMY_DATABASE_URL(self):
        if self.DATABASE_URL:
            if self.DATABASE_URL.startswith("postgresql://"):
                return self.DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1)
            return self.DATABASE_URL
            
        return str(URL.create(
            drivername="postgresql+psycopg2",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            database=self.POSTGRES_DB,
        ))

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache
def get_settings():
    return Settings()