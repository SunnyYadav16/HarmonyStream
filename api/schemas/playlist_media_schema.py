from pydantic import BaseModel, ConfigDict


class PlaylistMediaBase(BaseModel):
    playlist_id: int
    media_id: int

class PlaylistMediaCreate(PlaylistMediaBase):
    pass

class PlaylistMediaResponse(PlaylistMediaBase):
    model_config = ConfigDict(from_attributes=True)