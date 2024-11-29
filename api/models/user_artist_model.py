from sqlalchemy import Column, Integer, ForeignKey, Index
from sqlalchemy.orm import relationship
from api.database import Base

# Many-to-Many: User-Artist Follow Association Table
class UserArtist(Base):
    __tablename__ = "user_artists"
    __table_args__ = (
        Index('idx_user_artist_artist_id', 'artist_id'),
        Index('idx_user_artist_follower_id', 'follower_id'),
    )

    follower_id = Column(Integer, ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True)
    artist_id = Column(Integer, ForeignKey('artists.artist_id', ondelete='CASCADE'), primary_key=True)

    # Relationships
    follower = relationship("User")
    artist = relationship("Artist")