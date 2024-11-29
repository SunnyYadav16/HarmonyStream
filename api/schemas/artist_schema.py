from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict

class ArtistBase(BaseModel):
    artist_name: str = Field(..., min_length=1, max_length=255)
    artist_bio: Optional[str] = None
    profile_picture: Optional[str] = None

class ArtistCreate(ArtistBase):
    pass

class ArtistResponse(ArtistBase):
    artist_id: int
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)