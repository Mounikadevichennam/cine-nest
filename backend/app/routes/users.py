from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from app.database.connection import get_db
from app.auth.dependencies import get_current_user
from app.models.user import User, Profile
from app.models.movie import Genre, Actor
from app.schemas.user import ProfileCreate, ProfileResponse, UserResponse

class OnboardingRequest(BaseModel):
    preferred_language: str
    favourite_genre_ids: List[int] = []
    favourite_genre_names: List[str] = []
    favourite_actor_ids: List[int] = []

router = APIRouter(prefix="/api/v1/users", tags=["Users & Profiles"])

@router.post("/onboarding", response_model=UserResponse)
def save_onboarding(
    onboarding: OnboardingRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Save onboarding preferences (language, favourite genres, max 5 actors)."""
    current_user.preferred_language = onboarding.preferred_language
    
    # Update favourite genres
    if onboarding.favourite_genre_names:
        genres = db.query(Genre).filter(Genre.name.in_(onboarding.favourite_genre_names)).all()
        current_user.favourite_genres = genres
    elif onboarding.favourite_genre_ids:
        genres = db.query(Genre).filter(Genre.id.in_(onboarding.favourite_genre_ids)).all()
        current_user.favourite_genres = genres

    # Update favourite actors (max 5)
    if onboarding.favourite_actor_ids:
        actor_ids = onboarding.favourite_actor_ids[:5]
        actors = db.query(Actor).filter(Actor.id.in_(actor_ids)).all()
        current_user.favourite_actors = actors

    db.commit()
    db.refresh(current_user)
    return current_user

@router.get("/profiles", response_model=List[ProfileResponse])
def get_user_profiles(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all profile avatars for current user."""
    return db.query(Profile).filter(Profile.user_id == current_user.id).all()

@router.post("/profiles", response_model=ProfileResponse, status_code=status.HTTP_201_CREATED)
def create_user_profile(
    profile_in: ProfileCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new profile avatar."""
    new_profile = Profile(
        user_id=current_user.id,
        profile_name=profile_in.profile_name,
        avatar=profile_in.avatar or "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80"
    )
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    return new_profile

@router.put("/profiles/{profile_id}", response_model=ProfileResponse)
def update_user_profile(
    profile_id: int,
    profile_in: ProfileCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update profile name or avatar."""
    profile = db.query(Profile).filter(Profile.id == profile_id, Profile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    profile.profile_name = profile_in.profile_name
    if profile_in.avatar:
        profile.avatar = profile_in.avatar
    
    db.commit()
    db.refresh(profile)
    return profile
