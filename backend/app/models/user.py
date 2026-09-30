import enum
from sqlalchemy import Column, Integer, String, Enum as SQLEnum, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.connection import Base

class UserRole(str, enum.Enum):
    USER = "USER"
    ADMIN = "ADMIN"

# Junction Tables for User Preferences
user_favourite_genres = Table(
    'user_favourite_genres',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id', ondelete="CASCADE"), primary_key=True),
    Column('genre_id', Integer, ForeignKey('genres.id', ondelete="CASCADE"), primary_key=True)
)

user_favourite_actors = Table(
    'user_favourite_actors',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id', ondelete="CASCADE"), primary_key=True),
    Column('actor_id', Integer, ForeignKey('actors.id', ondelete="CASCADE"), primary_key=True)
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(SQLEnum(UserRole), default=UserRole.USER, nullable=False)
    preferred_language = Column(String(30), nullable=True) # Supported: Telugu, Hindi, Tamil, Malayalam, Kannada, English
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    profiles = relationship("Profile", back_populates="user", cascade="all, delete-orphan")
    favourite_genres = relationship("Genre", secondary=user_favourite_genres, backref="favourited_by_users")
    favourite_actors = relationship("Actor", secondary=user_favourite_actors, backref="favourited_by_users")

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    profile_name = Column(String(50), nullable=False)
    avatar = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="profiles")
