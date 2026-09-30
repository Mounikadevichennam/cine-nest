from sqlalchemy.orm import Session
from app.models.movie import Movie

class MovieService:
    @staticmethod
    def get_public_catalog(db: Session, skip: int = 0, limit: int = 50):
        return db.query(Movie).offset(skip).limit(limit).all()
