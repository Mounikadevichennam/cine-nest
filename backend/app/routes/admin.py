from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from app.database.connection import get_db
from app.auth.dependencies import require_admin
from app.models.user import User
from app.models.movie import Movie, Genre
from app.schemas.movie import MovieResponse
from app.schemas.admin import MovieCreateRequest, MovieUpdateRequest, AdminStatsResponse
from app.services.admin_service import AdminService

router = APIRouter(prefix="/api/v1/admin", tags=["Admin Portal"])

@router.get("/stats", response_model=AdminStatsResponse)
def admin_get_stats(
    current_admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Retrieve catalog statistics for admin dashboard."""
    total_movies = db.query(Movie).count()
    total_users = db.query(User).count()
    
    # Calculate popular language
    top_lang_res = db.query(Movie.language, func.count(Movie.id)).group_by(Movie.language).order_by(func.count(Movie.id).desc()).first()
    popular_lang = top_lang_res[0] if top_lang_res else "Telugu"

    return AdminStatsResponse(
        total_movies=total_movies,
        total_users=total_users,
        total_watch_hours=148.5,
        popular_language=popular_lang
    )

@router.post("/ingest-tmdb")
async def trigger_tmdb_ingestion(
    target_count: int = 20,
    current_admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Triggers TMDB data ingestion pipeline across 6 regional languages."""
    from app.services.tmdb_service import TMDBService
    result = await TMDBService.fetch_and_ingest_catalog(db, target_count_per_lang=target_count)
    return result

@router.get("/movies", response_model=List[MovieResponse])
def admin_get_movies(
    skip: int = 0,
    limit: int = 100,
    current_admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Retrieve full movie catalog for administrative management."""
    return AdminService.get_all_movies(db, skip=skip, limit=limit)

@router.post("/movies", response_model=MovieResponse, status_code=status.HTTP_201_CREATED)
def admin_create_movie(
    movie_in: MovieCreateRequest,
    current_admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Create a new movie entry with metadata, poster URL, and optional trailer URL."""
    return AdminService.create_movie(db, movie_in)

@router.put("/movies/{movie_id}", response_model=MovieResponse)
def admin_update_movie(
    movie_id: int,
    movie_in: MovieUpdateRequest,
    current_admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Update movie metadata, poster, or trailer."""
    return AdminService.update_movie(db, movie_id, movie_in)

@router.delete("/movies/{movie_id}")
def admin_delete_movie(
    movie_id: int,
    current_admin: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Delete a movie entry from the catalog."""
    AdminService.delete_movie(db, movie_id)
    return {"status": "success", "message": f"Movie {movie_id} deleted successfully"}
