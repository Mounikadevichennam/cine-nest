from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class WatchProgressUpdate(BaseModel):
    movie_id: Optional[int] = None
    progress_seconds: int = Field(..., ge=0)
    completion_percentage: float = Field(..., ge=0.0, le=100.0)

class RatingCreate(BaseModel):
    movie_id: int
    rating: int = Field(..., ge=1, le=5) # 1 to 5 scale

class LikeCreate(BaseModel):
    movie_id: int

class NotInterestedCreate(BaseModel):
    movie_id: int

class SearchCreate(BaseModel):
    search_query: str = Field(..., min_length=1, max_length=255)
