from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict

class GenreBase(BaseModel):
    genre_name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None

class GenreCreate(GenreBase):
    pass

class GenreResponse(GenreBase):
    genre_id: int
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)