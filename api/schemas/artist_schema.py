from typing import Optional

from pydantic import BaseModel, Field


class ArtistBase(BaseModel):
    artist_name: str = Field(..., min_length=1, max_length=255)
    artist_bio: Optional[str] = None
    profile_picture: Optional[str] = None

class ArtistCreate(ArtistBase):
    pass

class ArtistResponse(ArtistBase):
    artist_id: int
