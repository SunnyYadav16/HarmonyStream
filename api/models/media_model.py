import enum
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict
from sqlalchemy import Column, Integer, String, DateTime, Enum, Boolean, Time
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from api.database import Base


# Enum for Media Type
class MediaTypeEnum(enum.Enum):
    AUDIO = 'audio'
    VIDEO = 'video'


class Media(Base):
    __tablename__ = "media"

    media_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    media_title = Column(String(255), nullable=False, unique=True)
    media_type = Column(Enum(MediaTypeEnum), nullable=False)
    duration = Column(Time, nullable=True)
    s3_media_path = Column(String(255), nullable=True)
    thumbnail_image_path = Column(String(255), nullable=True)
    view_count = Column(Integer, default=0)
    is_premium_only = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)

    # Relationships
    favorites = relationship("Favorite", back_populates="media")
    comments = relationship("Comment", back_populates="media")
    ratings = relationship("Rating", back_populates="media")


class MediaBase(BaseModel):
    media_title: str = Field(..., min_length=1, max_length=255)
    media_type: MediaTypeEnum
    duration: Optional[time] = None
    s3_media_path: Optional[str] = None
    thumbnail_image_path: Optional[str] = None
    view_count: Optional[int] = 0
    is_premium_only: Optional[bool] = False


class MediaCreate(MediaBase):
    pass


class MediaResponse(MediaBase):
    media_id: int
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)
