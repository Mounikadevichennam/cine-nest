from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database.connection import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.models.movie import Movie
from app.models.activity import ContinueWatching, WatchHistory
from app.schemas.movie import MovieResponse
from app.recommendation.engine import RecommendationEngine

router = APIRouter(prefix="/api/v1/recommendations", tags=["Recommendation Engine"])

@router.get("/recommended", response_model=List[MovieResponse])
def get_recommended_for_you(
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Personalized 'Recommended For You' feed using 100-Point Hybrid Scoring Model."""
    return RecommendationEngine.get_recommendations_for_user(db, current_user, limit=limit)

@router.get("/because-you-watched", response_model=List[MovieResponse])
def get_because_you_watched(
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Content-based recommendations based on user's recent viewing history."""
    return RecommendationEngine.get_because_you_watched(db, current_user, limit=limit)

@router.get("/by-genres", response_model=List[MovieResponse])
def get_by_favourite_genres(
    limit: int = 15,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Recommendations matching user's onboarded favourite genres."""
    fav_genre_ids = [g.id for g in current_user.favourite_genres]
    if not fav_genre_ids:
        return db.query(Movie).filter(Movie.poster_url != None).order_by(Movie.imdb_rating.desc()).limit(limit).all()
    
    return db.query(Movie).filter(
        Movie.poster_url != None,
        Movie.genres.any(Movie.genres.property.mapper.class_.id.in_(fav_genre_ids))
    ).limit(limit).all()

@router.get("/by-actors", response_model=List[MovieResponse])
def get_by_favourite_actors(
    limit: int = 15,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Recommendations featuring user's onboarded favourite actors."""
    fav_actor_ids = [a.id for a in current_user.favourite_actors]
    if not fav_actor_ids:
        return db.query(Movie).filter(Movie.poster_url != None).order_by(Movie.imdb_vote_count.desc()).limit(limit).all()

    return db.query(Movie).filter(
        Movie.poster_url != None,
        Movie.movie_actors.any(Movie.movie_actors.property.mapper.class_.actor_id.in_(fav_actor_ids))
    ).limit(limit).all()

@router.get("/trending", response_model=List[MovieResponse])
def get_trending_now(limit: int = 15, db: Session = Depends(get_db)):
    """Trending / Popular movies feed ordered by vote count and rating."""
    return db.query(Movie).filter(Movie.poster_url != None).order_by(Movie.imdb_vote_count.desc(), Movie.imdb_rating.desc()).limit(limit).all()

@router.get("/new-releases", response_model=List[MovieResponse])
def get_new_releases(limit: int = 15, db: Session = Depends(get_db)):
    """New Releases feed (2024-2026)."""
    return db.query(Movie).filter(Movie.poster_url != None, Movie.release_year >= 2024).order_by(Movie.release_year.desc(), Movie.release_date.desc()).limit(limit).all()

@router.get("/continue-watching", response_model=List[MovieResponse])
def get_continue_watching(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Continue Watching feed for active user sessions."""
    records = db.query(ContinueWatching).filter(ContinueWatching.user_id == current_user.id).order_by(ContinueWatching.last_watched_at.desc()).all()
    movie_ids = [r.movie_id for r in records]
    if not movie_ids:
        return []
    return db.query(Movie).filter(Movie.id.in_(movie_ids)).all()
