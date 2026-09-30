from .auth import router as auth_router
from .users import router as users_router
from .movies import router as movies_router
from .admin import router as admin_router
from .recommendation import router as recommendation_router

__all__ = [
    "auth_router",
    "users_router",
    "movies_router",
    "admin_router",
    "recommendation_router",
]
