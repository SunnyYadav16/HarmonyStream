from datetime import datetime
from typing import List, Dict
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.schemas.media_schema import MediaResponse
from .. import database
from ..models.album_artist_model import AlbumArtist
from ..models.album_model import Album
from ..models.artist_model import Artist
from ..models.media_album_model import MediaAlbum
from ..models.media_artist_model import MediaArtist
from ..models.media_model import Media, MediaTypeEnum
from ..schemas.album_schema import AlbumResponse
from ..schemas.artist_schema import ArtistResponse

router = APIRouter()


@router.get("/media/tracks", response_model=Dict[str, List[MediaResponse]])
async def get_all_tracks_segregated(db: Session = Depends(database.get_db)):
    # Query all media items
    all_media = db.query(Media).filter(Media.deleted_at.is_(None)).all()

    # Initialize response structure
    segregated_media = {
        "audio": [],
        # "video": []
    }

    # Segregate media by type
    for media in all_media:
        if media.media_type == MediaTypeEnum.AUDIO:
            segregated_media["audio"].append(media.__dict__)
        # elif media.media_type == MediaTypeEnum.VIDEO:
        #     segregated_media["video"].append(media.__dict__)

    return segregated_media


@router.get("/media/albums", response_model=Dict[str, List[AlbumResponse]])
async def get_all_albums_segregated(db: Session = Depends(database.get_db)):
    # Query all media items
    all_album = db.query(Album).filter(Album.deleted_at.is_(None)).all()

    # Initialize response structure
    segregated_media = {
        "albums": [],
    }

    # Segregate media by type
    for album in all_album:
        segregated_media["albums"].append(album.__dict__)

    return segregated_media


@router.get("/media/artists", response_model=Dict[str, List[ArtistResponse]])
async def get_all_artists_segregated(db: Session = Depends(database.get_db)):
    # Query all media items
    all_artist = db.query(Artist).filter(Artist.deleted_at.is_(None)).all()

    # Initialize response structure
    segregated_media = {
        "artists": [],
    }

    # Segregate media by type
    for artist in all_artist:
        segregated_media["artists"].append(artist.__dict__)

    return segregated_media


@router.post("/insert_spotify_tracks")
def insert_spotify_tracks(spotify_data: dict, db: Session = Depends(database.get_db)):
    try:
        inserted_media = []
        tracks = spotify_data['tracks']['items']

        for track in tracks:
            # Insert or get Artist
            artist_data = track['artists'][0]
            artist = db.query(Artist).filter(Artist.artist_name == artist_data['name']).first()
            if not artist:
                artist = Artist(
                    artist_name=artist_data['name'],
                    artist_bio="",
                    profile_picture=artist_data.get('images', [None])[0] if 'images' in artist_data else None
                )
                db.add(artist)
                db.commit()
                db.refresh(artist)

            # Insert or get Album
            album_data = track['album']
            album = db.query(Album).filter(Album.album_title == album_data['name']).first()
            if not album:
                album = Album(
                    album_title=album_data['name'],
                    release_date=datetime.strptime(album_data['release_date'], '%Y-%m-%d'),
                    cover_art=album_data['images'][0]['url'] if album_data['images'] else None,
                    description="None"
                )
                db.add(album)
                db.commit()
                db.refresh(album)

            # Create Album-Artist Junction Entry
            album_artist = db.query(AlbumArtist).filter(
                AlbumArtist.album_id == album.album_id,
                AlbumArtist.artist_id == artist.artist_id
            ).first()
            if not album_artist:
                album_artist = AlbumArtist(
                    album_id=album.album_id,
                    artist_id=artist.artist_id
                )
                db.add(album_artist)

            # Insert Media
            media = Media(
                media_title=track['name'],
                media_type=MediaTypeEnum.AUDIO,
                duration=None,
                s3_media_path="None",
                thumbnail_image_path=album_data['images'][0]['url'] if album_data['images'] else None,
                view_count=track.get('popularity', 0),
                is_premium_only=False
            )
            db.add(media)
            db.commit()
            db.refresh(media)
            inserted_media.append(media.media_id)

            # Create Media-Album Junction Entry
            media_album = MediaAlbum(
                album_id=album.album_id,
                media_id=media.media_id
            )
            db.add(media_album)

            # Create Media-Artist Junction Entry
            media_artist = MediaArtist(
                media_id=media.media_id,
                artist_id=artist.artist_id
            )
            db.add(media_artist)

        db.commit()
        return {
            "message": "Successfully inserted tracks",
            "media_ids": inserted_media
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
