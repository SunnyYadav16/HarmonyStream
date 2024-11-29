from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict

# Pydantic Models
class AlbumBase(BaseModel):
    album_title: str = Field(..., min_length=1, max_length=255)
    release_date: Optional[date] = None
    cover_art: Optional[str] = None
    description: Optional[str] = None


class AlbumCreate(AlbumBase):
    pass


class AlbumResponse(AlbumBase):
    album_id: int
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)