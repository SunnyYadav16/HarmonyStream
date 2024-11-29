from sqlalchemy import Column, Integer, ForeignKey, Index
from sqlalchemy.orm import relationship
from api.database import Base

# Many-to-Many: Album-Artists Association Table
class AlbumArtist(Base):
    __tablename__ = "album_artists"
    __table_args__ = (
        Index('idx_album_artists_album_id', 'album_id'),
        Index('idx_album_artists_artist_id', 'artist_id'),
    )

    album_id = Column(Integer, ForeignKey('albums.album_id', ondelete='CASCADE'), primary_key=True)
    artist_id = Column(Integer, ForeignKey('artists.artist_id', ondelete='CASCADE'), primary_key=True)

    # Relationships
    album = relationship("Album")
    artist = relationship("Artist")
