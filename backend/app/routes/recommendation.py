from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database.connection import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.models.movie import Movie
from app.models.activity import ContinueWatching
from app.schemas.movie import MovieResponse
from app.recommendation.engine import RecommendationEngine
from app.services.tmdb_service import TMDBService

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
    fav_genres = [g.name for g in current_user.favourite_genres]
    pref_lang = current_user.preferred_language or "Telugu"
    if fav_genres:
        genre_name = fav_genres[0]
        live_movies = TMDBService.fetch_language_movies_live(pref_lang, genre_name=genre_name, limit=limit)
        if not live_movies:
            live_movies = TMDBService.fetch_genre_movies_live(genre_name, limit=limit)
        if live_movies:
            return live_movies
    # Fallback to preferred language discovery
    lang_movies = TMDBService.fetch_language_movies_live(pref_lang, limit=limit)
    if lang_movies:
        return lang_movies
    return TMDBService.fetch_trending_live(limit=limit)

@router.get("/by-actors", response_model=List[MovieResponse])
def get_by_favourite_actors(
    limit: int = 15,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Recommendations featuring user's onboarded favourite actors."""
    fav_actors = [a.name for a in current_user.favourite_actors]
    if fav_actors:
        actor_movies = []
        for aname in fav_actors:
            movies = TMDBService.fetch_actor_movies_live(aname, limit=limit)
            for m in movies:
                if not any((ex.get("tmdb_id") or ex.get("id")) == (m.get("tmdb_id") or m.get("id")) for ex in actor_movies):
                    actor_movies.append(m)
            if len(actor_movies) >= limit:
                break
        if actor_movies:
            return actor_movies[:limit]
    # Fallback to preferred language discovery rather than duplicating global trending
    pref_lang = current_user.preferred_language or "Telugu"
    lang_movies = TMDBService.fetch_language_movies_live(pref_lang, limit=limit)
    if lang_movies:
        return lang_movies
    return TMDBService.fetch_trending_live(limit=limit)

@router.get("/trending", response_model=List[MovieResponse])
def get_trending_now(limit: int = 15, db: Session = Depends(get_db)):
    """Live Trending / Popular movies feed."""
    return TMDBService.fetch_trending_live(limit=limit)

@router.get("/new-releases", response_model=List[MovieResponse])
def get_new_releases(limit: int = 15, db: Session = Depends(get_db)):
    """New Releases feed (2024-2026)."""
    return TMDBService.fetch_new_releases_live(limit=limit)

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
    movies = db.query(Movie).filter(Movie.id.in_(movie_ids)).all()
    # Enrich any movie with missing poster
    for m in movies:
        if not m.poster_url or not m.poster_url.startswith("http") or "unsplash" in m.poster_url:
            live = TMDBService.get_tmdb_movie_details_live(m.tmdb_id or m.id)
            if live and live.get("poster_url"):
                m.poster_url = live["poster_url"]
                m.backdrop_url = live.get("backdrop_url") or m.backdrop_url
    try:
        db.commit()
    except Exception:
        db.rollback()
    return movies
