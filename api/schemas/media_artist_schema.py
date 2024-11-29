from pydantic import BaseModel, ConfigDict


class MediaArtistBase(BaseModel):
    media_id: int
    artist_id: int

class MediaArtistCreate(MediaArtistBase):
    pass

class MediaArtistResponse(MediaArtistBase):
    model_config = ConfigDict(from_attributes=True)