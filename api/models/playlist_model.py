
from sqlalchemy import Column, Integer, DateTime, ForeignKey, String, Text, Boolean, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from api.database import Base

class Playlist(Base):
    __tablename__ = "playlists"
    __table_args__ = (
        Index('idx_playlist_user_id', 'user_id'),
        Index('idx_playlist_is_public', 'is_public'),
    )

    playlist_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    playlist_title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    is_public = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)

    # Relationships
    user = relationship("User")
    playlist_media = relationship("PlaylistMedia", back_populates="playlist")
