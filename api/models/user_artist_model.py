from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from api.database import Base

# Many-to-Many: User-Artist Follow Association Table
class UserArtist(Base):
    __tablename__ = "user_artists"

    follower_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True)
    artist_id = Column(Integer, ForeignKey('artists.artist_id', ondelete='CASCADE'), primary_key=True)

    # Relationships
    follower = relationship("User")
    artist = relationship("Artist")