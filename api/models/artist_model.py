from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from api.database import Base

class Artist(Base):
    __tablename__ = "artists"

    artist_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    artist_name = Column(String(255), nullable=False, unique=True)
    artist_bio = Column(Text, nullable=True)
    profile_picture = Column(String(255), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)


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