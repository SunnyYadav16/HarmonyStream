from pydantic import BaseModel, ConfigDict
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from api.database import Base

# Many-to-Many: Media-Artists Association Table
class MediaArtist(Base):
    __tablename__ = "media_artists"

    media_id = Column(Integer, ForeignKey('media.media_id', ondelete='CASCADE'), primary_key=True)
    artist_id = Column(Integer, ForeignKey('artists.artist_id', ondelete='CASCADE'), primary_key=True)

    # Relationships
    media = relationship("Media")
    artist = relationship("Artist")


class MediaArtistBase(BaseModel):
    media_id: int
    artist_id: int

class MediaArtistCreate(MediaArtistBase):
    pass

class MediaArtistResponse(MediaArtistBase):
    model_config = ConfigDict(from_attributes=True)