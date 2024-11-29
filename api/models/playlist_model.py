from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict
from sqlalchemy import Column, Integer, DateTime, ForeignKey, String, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from api.database import Base

class Playlist(Base):
    __tablename__ = "playlists"

    playlist_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    playlist_title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    is_public = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)

    # Relationships
    user = relationship("User")


class PlaylistBase(BaseModel):
    playlist_title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    is_public: Optional[bool] = False
    user_id: int

class PlaylistCreate(PlaylistBase):
    pass

class PlaylistResponse(PlaylistBase):
    playlist_id: int
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)