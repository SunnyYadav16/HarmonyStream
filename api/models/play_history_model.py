
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from api.database import Base


# Media History Table
class PlayHistory(Base):
    __tablename__ = "play_history"

    history_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    media_id = Column(Integer, ForeignKey('media.media_id', ondelete='CASCADE'), nullable=False)
    played_at = Column(DateTime, server_default=func.now())

    # Relationships
    user = relationship("User")
    media = relationship("Media")

