from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.connection import get_db
from app.auth.dependencies import get_current_user, get_optional_current_user, require_admin
from app.models.user import User
from app.models.movie import Movie, Genre, Actor
from app.models.activity import WatchHistory, Like, NotInterested, Rating, SearchHistory, ContinueWatching, RecentActivity
from app.schemas.movie import MovieResponse
from app.schemas.activity import WatchProgressUpdate, RatingCreate, LikeCreate, NotInterestedCreate
from app.services.tmdb_service import TMDBService

router = APIRouter(prefix="/api/v1/movies", tags=["Public Movie Catalog"])

@router.get("", response_model=List[MovieResponse])
def get_movies(
    skip: int = 0,
    limit: int = 50,
    page: int = 1,
    language: Optional[str] = None,
    genre: Optional[str] = None,
    year: Optional[int] = None,
    min_rating: Optional[float] = None,
    db: Session = Depends(get_db)
):
    """Retrieve catalog movies via dynamic live TMDB API search/discovery."""
    if genre:
        live_results = TMDBService.fetch_genre_movies_live(genre, page=page, limit=limit)
        if live_results:
            return live_results
    elif year or language:
        q_term = str(year) if year else language
        live_results = TMDBService.search_tmdb_live(q_term, page=page)
        if live_results:
            return live_results

    # Fallback to live trending movies
    live_trending = TMDBService.fetch_trending_live(page=page, limit=limit)
    if live_trending:
        return live_trending

    return db.query(Movie).filter(Movie.poster_url != None).offset(skip).limit(limit).all()

@router.get("/search", response_model=List[MovieResponse])
def search_movies(
    q: str = Query(..., min_length=1),
    page: int = Query(default=1, ge=1),
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db)
):
    """Dynamic Live TMDB Search Endpoint: Searches TMDB live without polluting MySQL."""
    if current_user:
        try:
            search_rec = SearchHistory(user_id=current_user.id, search_query=q)
            db.add(search_rec)
            db.commit()
        except Exception:
            db.rollback()

    live_results = TMDBService.search_tmdb_live(q, page=page)
    if live_results:
        return live_results

    # Fallback search on existing local MySQL records if TMDB returns empty
    search_term = f"%{q.strip()}%"
    q_filter = (
        Movie.title.ilike(search_term) |
        Movie.original_title.ilike(search_term) |
        Movie.language.ilike(search_term) |
        Movie.storyline.ilike(search_term) |
        Movie.genres.any(Genre.name.ilike(search_term))
    )
    return db.query(Movie).filter(Movie.poster_url != None, q_filter).limit(40).all()

@router.get("/{movie_id}", response_model=MovieResponse)
def get_movie_details(movie_id: int, db: Session = Depends(get_db)):
    """Retrieve movie details by ID or TMDB ID live."""
    movie = db.query(Movie).filter((Movie.id == movie_id) | (Movie.tmdb_id == movie_id)).first()
    if movie:
        return TMDBService.enrich_movie_details(db, movie)

    live_detail = TMDBService.get_tmdb_movie_details_live(movie_id)
    if live_detail:
        return live_detail

    raise HTTPException(status_code=404, detail="Movie not found")

@router.post("/{movie_id}/watch")
def record_watch_progress(
    movie_id: int,
    progress: WatchProgressUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Track watch progress, completion percentage, and continue watching state."""
    movie = TMDBService.ensure_movie_in_db(db, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    target_id = movie.id
    is_completed = progress.completion_percentage >= 90.0

    # Watch History
    wh = db.query(WatchHistory).filter(WatchHistory.user_id == current_user.id, WatchHistory.movie_id == target_id).first()
    if not wh:
        wh = WatchHistory(
            user_id=current_user.id,
            movie_id=target_id,
            progress_seconds=progress.progress_seconds,
            completion_percentage=progress.completion_percentage,
            completed=is_completed,
            watch_count=1
        )
        db.add(wh)
    else:
        wh.progress_seconds = max(wh.progress_seconds, progress.progress_seconds)
        wh.completion_percentage = max(wh.completion_percentage, progress.completion_percentage)
        wh.completed = wh.completed or is_completed
        wh.watch_count = (wh.watch_count or 1) + 1

    # Continue Watching (Upsert)
    cw = db.query(ContinueWatching).filter(ContinueWatching.user_id == current_user.id, ContinueWatching.movie_id == target_id).first()
    if not is_completed:
        if not cw:
            cw = ContinueWatching(
                user_id=current_user.id,
                movie_id=target_id,
                progress_seconds=progress.progress_seconds,
                completion_percentage=progress.completion_percentage
            )
            db.add(cw)
        else:
            cw.progress_seconds = progress.progress_seconds
            cw.completion_percentage = progress.completion_percentage
    elif cw:
        db.delete(cw)

    # Log Recent Activity
    activity = RecentActivity(user_id=current_user.id, movie_id=target_id, activity_type="WATCHED")
    db.add(activity)

    db.commit()
    return {"status": "success", "completed": is_completed}

@router.post("/{movie_id}/like")
def toggle_like(
    movie_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Toggle Like status on a movie."""
    movie = TMDBService.ensure_movie_in_db(db, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    target_id = movie.id
    lk = db.query(Like).filter(Like.user_id == current_user.id, Like.movie_id == target_id).first()
    if lk:
        db.delete(lk)
        message = "Unliked movie"
        liked = False
    else:
        lk = Like(user_id=current_user.id, movie_id=target_id)
        db.add(lk)
        message = "Liked movie"
        liked = True
    db.commit()
    return {"status": "success", "message": message, "liked": liked}

@router.post("/{movie_id}/not-interested")
def mark_not_interested(
    movie_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Mark a movie as Not Interested (applies negative preference weight)."""
    movie = TMDBService.ensure_movie_in_db(db, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    target_id = movie.id
    ni = db.query(NotInterested).filter(NotInterested.user_id == current_user.id, NotInterested.movie_id == target_id).first()
    if not ni:
        ni = NotInterested(user_id=current_user.id, movie_id=target_id)
        db.add(ni)
        db.commit()
    return {"status": "success", "message": "Marked movie as Not Interested"}

@router.post("/{movie_id}/rate")
def rate_movie(
    movie_id: int,
    rating_in: RatingCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Submit a 1 to 5 user rating."""
    movie = TMDBService.ensure_movie_in_db(db, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    target_id = movie.id
    r = db.query(Rating).filter(Rating.user_id == current_user.id, Rating.movie_id == target_id).first()
    if not r:
        r = Rating(user_id=current_user.id, movie_id=target_id, rating=rating_in.rating)
        db.add(r)
    else:
        r.rating = rating_in.rating
    db.commit()
    return {"status": "success", "rating": rating_in.rating}
