from datetime import datetime, time
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict

from api.models.media_model import MediaTypeEnum


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
