from pydantic import BaseModel, ConfigDict


class MediaGenreBase(BaseModel):
    media_id: int
    genre_id: int

class MediaGenreCreate(MediaGenreBase):
    pass

class MediaGenreResponse(MediaGenreBase):
    model_config = ConfigDict(from_attributes=True)