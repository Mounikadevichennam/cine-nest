from sqlalchemy import Column, Integer, String, Float, Text, Date, DateTime, ForeignKey, Table, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.connection import Base

# Junction Table for Movie <-> Genre (N:M)
movie_genres = Table(
    'movie_genres',
    Base.metadata,
    Column('movie_id', Integer, ForeignKey('movies.id', ondelete="CASCADE"), primary_key=True),
    Column('genre_id', Integer, ForeignKey('genres.id', ondelete="CASCADE"), primary_key=True)
)

class MovieActor(Base):
    """Junction Model for Movie <-> Actor with character_name support."""
    __tablename__ = "movie_actors"

    movie_id = Column(Integer, ForeignKey("movies.id", ondelete="CASCADE"), primary_key=True)
    actor_id = Column(Integer, ForeignKey("actors.id", ondelete="CASCADE"), primary_key=True)
    character_name = Column(String(100), nullable=True)

    movie = relationship("Movie", back_populates="movie_actors")
    actor = relationship("Actor", back_populates="movie_actors")

class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True, nullable=False)

class Actor(Base):
    __tablename__ = "actors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    profile_image_url = Column(String(500), nullable=True)

    movie_actors = relationship("MovieActor", back_populates="actor", cascade="all, delete-orphan")

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    imdb_id = Column(String(20), unique=True, index=True, nullable=True)
    tmdb_id = Column(Integer, unique=True, index=True, nullable=True)
    title = Column(String(255), index=True, nullable=False)
    original_title = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    storyline = Column(Text, nullable=True)
    release_date = Column(Date, nullable=True)
    release_year = Column(Integer, index=True, nullable=False) # Feature films 2016-2026
    imdb_rating = Column(Float, default=0.0, index=True)
    imdb_vote_count = Column(Integer, default=0)
    popularity = Column(Float, default=0.0)
    poster_url = Column(String(500), nullable=False) # Required for catalog insertion
    backdrop_url = Column(String(500), nullable=True)
    trailer_url = Column(String(500), nullable=True)
    video_key = Column(String(100), nullable=True)
    video_site = Column(String(50), nullable=True)
    video_type = Column(String(50), nullable=True)
    is_official_trailer = Column(Boolean, default=False)
    language = Column(String(50), index=True, nullable=False)
    original_language = Column(String(20), nullable=True)
    country = Column(String(100), nullable=True, default="India")
    production_company = Column(String(150), nullable=True)
    director = Column(String(150), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    genres = relationship("Genre", secondary=movie_genres, backref="movies")
    movie_actors = relationship("MovieActor", back_populates="movie", cascade="all, delete-orphan")
