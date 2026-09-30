from pydantic import BaseModel
from typing import Optional, List
from .movie import MovieBase

class MovieCreateRequest(MovieBase):
    genre_names: List[str] = []
    actor_names: List[str] = []

class MovieUpdateRequest(BaseModel):
    imdb_id: Optional[str] = None
    title: Optional[str] = None
    language: Optional[str] = None
    release_year: Optional[int] = None
    imdb_rating: Optional[float] = None
    imdb_vote_count: Optional[int] = None
    imdb_votes: Optional[int] = None
    storyline: Optional[str] = None
    poster_url: Optional[str] = None
    trailer_url: Optional[str] = None
    genre_names: Optional[List[str]] = None
    actor_names: Optional[List[str]] = None

class AdminStatsResponse(BaseModel):
    total_movies: int
    total_users: int
    total_watch_hours: float
    popular_language: str
