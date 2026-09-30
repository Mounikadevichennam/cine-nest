from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.movie import Movie, Genre, Actor
from app.models.user import User
from app.schemas.admin import MovieCreateRequest, MovieUpdateRequest

class AdminService:
    @staticmethod
    def get_all_movies(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Movie).offset(skip).limit(limit).all()

    @staticmethod
    def create_movie(db: Session, movie_in: MovieCreateRequest) -> Movie:
        db_movie = Movie(
            imdb_id=movie_in.imdb_id,
            title=movie_in.title,
            language=movie_in.language,
            release_year=movie_in.release_year,
            release_date=movie_in.release_date,
            imdb_rating=movie_in.imdb_rating,
            imdb_vote_count=getattr(movie_in, "imdb_vote_count", getattr(movie_in, "imdb_votes", 0)),
            storyline=movie_in.storyline,
            poster_url=movie_in.poster_url,
            trailer_url=movie_in.trailer_url,
        )
        db.add(db_movie)
        db.commit()
        db.refresh(db_movie)
        return db_movie

    @staticmethod
    def update_movie(db: Session, movie_id: int, movie_in: MovieUpdateRequest) -> Movie:
        movie = db.query(Movie).filter(Movie.id == movie_id).first()
        if not movie:
            raise HTTPException(status_code=404, detail="Movie not found")
        
        update_data = movie_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if hasattr(movie, field) and value is not None:
                setattr(movie, field, value)

        db.commit()
        db.refresh(movie)
        return movie

    @staticmethod
    def delete_movie(db: Session, movie_id: int) -> bool:
        movie = db.query(Movie).filter(Movie.id == movie_id).first()
        if not movie:
            raise HTTPException(status_code=404, detail="Movie not found")
        db.delete(movie)
        db.commit()
        return True
