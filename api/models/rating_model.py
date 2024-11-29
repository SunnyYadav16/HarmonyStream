
from sqlalchemy import Column, Integer, DateTime, ForeignKey, CheckConstraint, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from api.database import Base


class Rating(Base):
    __tablename__ = "ratings"
    __table_args__ = (
        Index('idx_ratings_user_id', 'user_id'),
        Index('idx_ratings_media_id', 'media_id'),
        Index('idx_ratings_rating', 'rating'),
        CheckConstraint('rating BETWEEN 1 AND 5', name='valid_rating_range'),
    )

    rating_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    media_id = Column(Integer, ForeignKey('media.media_id', ondelete='CASCADE'), nullable=False)
    rating = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)

    # Relationships
    user = relationship("User")
    media = relationship("Media", back_populates="ratings")

