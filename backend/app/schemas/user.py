from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from app.models.user import UserRole

class UserSignup(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)
    preferred_language: Optional[str] = "Telugu"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class ProfileCreate(BaseModel):
    profile_name: str = Field(..., min_length=1, max_length=50)
    avatar: Optional[str] = None

class ProfileResponse(BaseModel):
    id: int
    user_id: int
    profile_name: str
    avatar: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: UserRole
    preferred_language: Optional[str] = None
    created_at: datetime
    profiles: List[ProfileResponse] = []

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
