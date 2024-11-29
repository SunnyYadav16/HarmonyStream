from pydantic import BaseModel, ConfigDict
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from api.database import Base

# Many-to-Many: Media-Genres Association Table
class MediaGenre(Base):
    __tablename__ = "media_genres"

    media_id = Column(Integer, ForeignKey('media.media_id', ondelete='CASCADE'), primary_key=True)
    genre_id = Column(Integer, ForeignKey('genres.genre_id', ondelete='CASCADE'), primary_key=True)

    # Relationships
    media = relationship("Media")
    genre = relationship("Genre")


class MediaGenreBase(BaseModel):
    media_id: int
    genre_id: int

class MediaGenreCreate(MediaGenreBase):
    pass

class MediaGenreResponse(MediaGenreBase):
    model_config = ConfigDict(from_attributes=True)