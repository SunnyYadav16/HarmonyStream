from sqlalchemy import Column, Integer, ForeignKey, Index
from sqlalchemy.orm import relationship

from api.database import Base


class MediaAlbum(Base):
    __tablename__ = "media_albums"
    __table_args__ = (
        Index('idx_media_albums_media_id', 'media_id'),
    )

    album_id = Column(Integer, ForeignKey('albums.album_id', ondelete='CASCADE'), primary_key=True)
    media_id = Column(Integer, ForeignKey('media.media_id', ondelete='CASCADE'), primary_key=True)

    # Relationships
    album = relationship("Album")
    media = relationship("Media")

