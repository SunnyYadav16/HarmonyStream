from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict

class PlaylistBase(BaseModel):
    playlist_title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    is_public: Optional[bool] = False

class PlaylistCreate(PlaylistBase):
    pass

class PlaylistResponse(PlaylistBase):
    playlist_id: int
    created_at: datetime

