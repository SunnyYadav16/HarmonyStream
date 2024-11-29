from pydantic import BaseModel, ConfigDict
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from api.database import Base


class MediaAlbum(Base):
    __tablename__ = "media_albums"

    album_id = Column(Integer, ForeignKey('albums.album_id', ondelete='CASCADE'), primary_key=True)
    media_id = Column(Integer, ForeignKey('media.media_id', ondelete='CASCADE'), primary_key=True)

    # Relationships
    album = relationship("Album")
    media = relationship("Media")


class MediaAlbumBase(BaseModel):
    album_id: int
    media_id: int


class MediaAlbumCreate(MediaAlbumBase):
    pass


class MediaAlbumResponse(MediaAlbumBase):
    model_config = ConfigDict(from_attributes=True)
