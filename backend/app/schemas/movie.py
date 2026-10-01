from pydantic import BaseModel, HttpUrl, Field
from typing import Optional, List
from datetime import date, datetime

class GenreSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class ActorSchema(BaseModel):
    id: int
    name: str
    profile_image_url: Optional[str] = None

    class Config:
        from_attributes = True

class MovieBase(BaseModel):
    imdb_id: Optional[str] = None
    tmdb_id: Optional[int] = None
    title: str = Field(..., min_length=1, max_length=255)
    original_title: Optional[str] = None
    description: Optional[str] = None
    storyline: Optional[str] = None
    release_date: Optional[date] = None
    release_year: int = Field(..., ge=1800, le=2100)
    imdb_rating: Optional[float] = Field(default=0.0, ge=0.0, le=10.0)
    imdb_vote_count: Optional[int] = Field(default=0, ge=0)
    popularity: Optional[float] = 0.0
    poster_url: str = Field(..., description="Poster URL is required for catalog insertion")
    backdrop_url: Optional[str] = None
    trailer_url: Optional[str] = None
    video_key: Optional[str] = None
    video_site: Optional[str] = None
    video_type: Optional[str] = None
    is_official_trailer: Optional[bool] = False
    language: str = Field(..., description="Movie audio language")
    original_language: Optional[str] = None
    country: Optional[str] = "India"
    production_company: Optional[str] = None
    director: Optional[str] = None

class MovieCreate(MovieBase):
    genre_names: List[str] = []
    actor_names: List[str] = []

class MovieUpdate(BaseModel):
    imdb_id: Optional[str] = None
    tmdb_id: Optional[int] = None
    title: Optional[str] = None
    original_title: Optional[str] = None
    description: Optional[str] = None
    storyline: Optional[str] = None
    release_date: Optional[date] = None
    release_year: Optional[int] = Field(default=None, ge=1800, le=2100)
    imdb_rating: Optional[float] = None
    imdb_vote_count: Optional[int] = None
    popularity: Optional[float] = None
    poster_url: Optional[str] = None
    backdrop_url: Optional[str] = None
    trailer_url: Optional[str] = None
    video_key: Optional[str] = None
    video_site: Optional[str] = None
    video_type: Optional[str] = None
    is_official_trailer: Optional[bool] = None
    language: Optional[str] = None
    original_language: Optional[str] = None
    country: Optional[str] = None
    production_company: Optional[str] = None
    director: Optional[str] = None
    genre_names: Optional[List[str]] = None
    actor_names: Optional[List[str]] = None

class MovieResponse(MovieBase):
    id: int
    created_at: datetime
    updated_at: datetime
    genres: List[GenreSchema] = []

    class Config:
        from_attributes = True
