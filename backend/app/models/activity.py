from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.connection import Base

class WatchHistory(Base):
    __tablename__ = "watch_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id", ondelete="CASCADE"), nullable=False, index=True)
    progress_seconds = Column(Integer, default=0)
    completion_percentage = Column(Float, default=0.0)
    watched_at = Column(DateTime, default=datetime.utcnow)
    completed = Column(Boolean, default=False)
    watch_count = Column(Integer, default=1)

    user = relationship("User", backref="watch_histories")
    movie = relationship("Movie", backref="watch_histories")

class Like(Base):
    __tablename__ = "likes"
    __table_args__ = (
        UniqueConstraint('user_id', 'movie_id', name='uq_user_movie_like'),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", backref="likes")
    movie = relationship("Movie", backref="likes")

class NotInterested(Base):
    __tablename__ = "not_interested"
    __table_args__ = (
        UniqueConstraint('user_id', 'movie_id', name='uq_user_movie_not_interested'),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", backref="not_interested_items")
    movie = relationship("Movie", backref="not_interested_items")

class Rating(Base):
    __tablename__ = "ratings"
    __table_args__ = (
        UniqueConstraint('user_id', 'movie_id', name='uq_user_movie_rating'),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id", ondelete="CASCADE"), nullable=False, index=True)
    rating = Column(Integer, nullable=False) # 1 to 5 rating
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", backref="ratings")
    movie = relationship("Movie", backref="ratings")

class SearchHistory(Base):
    __tablename__ = "search_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    search_query = Column(String(255), nullable=False)
    searched_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", backref="searches")

class ContinueWatching(Base):
    __tablename__ = "continue_watching"
    __table_args__ = (
        UniqueConstraint('user_id', 'movie_id', name='uq_user_movie_continue_watching'),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id", ondelete="CASCADE"), nullable=False, index=True)
    progress_seconds = Column(Integer, default=0)
    completion_percentage = Column(Float, default=0.0)
    last_watched_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", backref="continue_watching_items")
    movie = relationship("Movie", backref="continue_watching_items")

class RecentActivity(Base):
    __tablename__ = "recent_activities"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id", ondelete="CASCADE"), nullable=True, index=True)
    activity_type = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", backref="recent_activities")
    movie = relationship("Movie", backref="recent_activities")
