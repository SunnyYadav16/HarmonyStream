from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from api.database import Base


class Favorite(Base):
    __tablename__ = "favorites"

    favorite_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    media_id = Column(Integer, ForeignKey('media.media_id', ondelete='CASCADE'), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)

    # Relationships
    user = relationship("User")
    media = relationship("Media", back_populates="favorites")
