from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict

class RatingBase(BaseModel):
    user_id: int
    media_id: int
    rating: int = Field(..., ge=1, le=5)


class RatingCreate(RatingBase):
    pass


class RatingResponse(RatingBase):
    rating_id: int
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)