from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict
from sqlalchemy import Column, Integer, DateTime, String, Text
from sqlalchemy.sql import func
from api.database import Base

class Genre(Base):
    __tablename__ = "genres"

    genre_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    genre_name = Column(String(255), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)


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