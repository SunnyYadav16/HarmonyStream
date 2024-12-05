from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

class FavoriteBase(BaseModel):
    # user_id: int
    media_id: int


class FavoriteCreate(FavoriteBase):
    media_title: str


class FavoriteResponse(FavoriteBase):
    favorite_id: int

    class Config:
        orm_mode = True