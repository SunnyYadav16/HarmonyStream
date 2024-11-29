# Add these to your existing models to establish relationships
from api.models.album_model import Album
from api.models.artist_model import Artist
from api.models.genre_model import Genre
from api.models.media_model import Media
from api.models.playlist_model import Playlist
from api.models.user_model import User


def add_relationships_to_existing_models():
    # Example of how to add relationships to existing models
    from sqlalchemy.orm import relationship

    # In Album model
    Album.media = relationship("MediaAlbum", back_populates="album")
    Album.artists = relationship("AlbumArtist", back_populates="album")

    # In Media model
    Media.albums = relationship("MediaAlbum", back_populates="media")
    Media.genres = relationship("MediaGenre", back_populates="media")
    Media.artists = relationship("MediaArtist", back_populates="media")
    Media.playlists = relationship("PlaylistMedia", back_populates="media")

    # In Artist model
    Artist.media = relationship("MediaArtist", back_populates="artist")
    Artist.albums = relationship("AlbumArtist", back_populates="artist")
    Artist.followers = relationship("UserArtist", back_populates="artist")

    # In User model
    User.followed_artists = relationship("UserArtist", back_populates="follower")
    User.play_history = relationship("PlayHistory", back_populates="user")

    # In Playlist model
    Playlist.media = relationship("PlaylistMedia", back_populates="playlist")

    # In Genre model
    Genre.media = relationship("MediaGenre", back_populates="genre")
