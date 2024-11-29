from pydantic import BaseModel, ConfigDict
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from api.database import Base

# Many-to-Many: Album-Artists Association Table
class AlbumArtist(Base):
    __tablename__ = "album_artists"

    album_id = Column(Integer, ForeignKey('albums.album_id', ondelete='CASCADE'), primary_key=True)
    artist_id = Column(Integer, ForeignKey('artists.artist_id', ondelete='CASCADE'), primary_key=True)

    # Relationships
    album = relationship("Album")
    artist = relationship("Artist")

class AlbumArtistBase(BaseModel):
    album_id: int
    artist_id: int

class AlbumArtistCreate(AlbumArtistBase):
    pass

class AlbumArtistResponse(AlbumArtistBase):
    model_config = ConfigDict(from_attributes=True)