from datetime import datetime

from pydantic import BaseModel, ConfigDict

class PlayHistoryBase(BaseModel):
    user_id: int
    media_id: int


class PlayHistoryCreate(PlayHistoryBase):
    pass


class PlayHistoryResponse(PlayHistoryBase):
    history_id: int
    played_at: datetime

    model_config = ConfigDict(from_attributes=True)