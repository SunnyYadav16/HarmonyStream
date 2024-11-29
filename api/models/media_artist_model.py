from sqlalchemy import Column, Integer, ForeignKey, Index
from sqlalchemy.orm import relationship
from api.database import Base

# Many-to-Many: Media-Artists Association Table
class MediaArtist(Base):
    __tablename__ = "media_artists"
    __table_args__ = (
        Index('idx_media_artists_media_id', 'media_id'),
        Index('idx_media_artists_artist_id', 'artist_id'),
    )

    media_id = Column(Integer, ForeignKey('media.media_id', ondelete='CASCADE'), primary_key=True)
    artist_id = Column(Integer, ForeignKey('artists.artist_id', ondelete='CASCADE'), primary_key=True)

    # Relationships
    media = relationship("Media")
    artist = relationship("Artist")
