from pydantic import BaseModel, ConfigDict


class AlbumArtistBase(BaseModel):
    album_id: int
    artist_id: int

class AlbumArtistCreate(AlbumArtistBase):
    pass

class AlbumArtistResponse(AlbumArtistBase):
    model_config = ConfigDict(from_attributes=True)