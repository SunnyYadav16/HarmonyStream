from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict
from sqlalchemy import Column, Integer, String, Text, DateTime, CheckConstraint
from sqlalchemy.sql import func

from api.database import Base


# SQLAlchemy Models
class Album(Base):
    __tablename__ = "albums"

    album_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    album_title = Column(String(255), nullable=False)
    release_date = Column(DateTime)
    cover_art = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)

    __table_args__ = (
        CheckConstraint('album_title IS NOT NULL', name='album_title_not_null'),
        CheckConstraint('release_date IS NOT NULL', name='release_date_not_null'),
    )


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
