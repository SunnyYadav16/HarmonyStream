from datetime import datetime

from pydantic import BaseModel, ConfigDict
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


class PlayHistoryBase(BaseModel):
    user_id: int
    media_id: int


class PlayHistoryCreate(PlayHistoryBase):
    pass


class PlayHistoryResponse(PlayHistoryBase):
    history_id: int
    played_at: datetime

    model_config = ConfigDict(from_attributes=True)
