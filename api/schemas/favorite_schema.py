from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

class FavoriteBase(BaseModel):
    user_id: int
    media_id: int


class FavoriteCreate(FavoriteBase):
    pass


class FavoriteResponse(FavoriteBase):
    favorite_id: int
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)