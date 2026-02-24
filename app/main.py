from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.db.init_db import init_db
from app.routers import auth_router, track_router
from app.routers import auth_router, track_router, analytics_router

settings = get_settings()

app = FastAPI(title=settings.PROJECT_NAME, version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    init_db()


app.include_router(auth_router)
app.include_router(track_router)
app.include_router(analytics_router)


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "healthy"}