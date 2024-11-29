from pydantic import BaseModel, ConfigDict
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from api.database import Base

# Many-to-Many: Playlist-Media Association Table
class PlaylistMedia(Base):
    __tablename__ = "playlist_media"

    playlist_id = Column(Integer, ForeignKey('playlists.playlist_id', ondelete='CASCADE'), primary_key=True)
    media_id = Column(Integer, ForeignKey('media.media_id', ondelete='CASCADE'), primary_key=True)

    # Relationships
    playlist = relationship("Playlist")
    media = relationship("Media")

class PlaylistMediaBase(BaseModel):
    playlist_id: int
    media_id: int

class PlaylistMediaCreate(PlaylistMediaBase):
    pass

class PlaylistMediaResponse(PlaylistMediaBase):
    model_config = ConfigDict(from_attributes=True)