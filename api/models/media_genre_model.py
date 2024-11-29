from sqlalchemy import Column, Integer, ForeignKey, Index
from sqlalchemy.orm import relationship
from api.database import Base

# Many-to-Many: Media-Genres Association Table
class MediaGenre(Base):
    __tablename__ = "media_genres"
    __table_args__ = (
        Index('idx_media_genres_media_id', 'media_id'),
        Index('idx_media_genres_genre_id', 'genre_id'),
    )

    media_id = Column(Integer, ForeignKey('media.media_id', ondelete='CASCADE'), primary_key=True)
    genre_id = Column(Integer, ForeignKey('genres.genre_id', ondelete='CASCADE'), primary_key=True)

    # Relationships
    media = relationship("Media")
    genre = relationship("Genre")
