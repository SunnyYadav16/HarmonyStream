from pydantic import BaseModel, ConfigDict


class MediaAlbumBase(BaseModel):
    album_id: int
    media_id: int


class MediaAlbumCreate(MediaAlbumBase):
    pass


class MediaAlbumResponse(MediaAlbumBase):
    model_config = ConfigDict(from_attributes=True)
