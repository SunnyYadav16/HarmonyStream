from pydantic import BaseModel, ConfigDict


class UserArtistBase(BaseModel):
    follower_id: int
    artist_id: int

class UserArtistCreate(UserArtistBase):
    pass

class UserArtistResponse(UserArtistBase):
    model_config = ConfigDict(from_attributes=True)