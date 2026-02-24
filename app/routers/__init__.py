from app.routers.auth import router as auth_router
from app.routers.track import router as track_router
from app.routers.analytics import router as analytics_router

__all__ = ["auth_router", "track_router", "analytics_router"]