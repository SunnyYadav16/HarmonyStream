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
