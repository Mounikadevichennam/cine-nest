from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.settings import settings
from app.routes import auth_router, users_router, movies_router, admin_router, recommendation_router

app = FastAPI(
    title="CineNest REST API",
    description="Personalized OTT Subscriber & Recommendation System API",
    version="1.0.0",
)

# Configure CORS for Frontend integration (Vercel & Localhost)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(movies_router)
app.include_router(admin_router)
app.include_router(recommendation_router)

@app.get("/")
def read_root():
    return {
        "status": "online",
        "app": "CineNest OTT Backend",
        "version": "1.0.0",
        "docs_url": "/docs"
    }

@app.get("/api/v1/health")
def health_check():
    """Simple backend health endpoint."""
    return {
        "status": "ok",
        "service": "CineNest API"
    }
