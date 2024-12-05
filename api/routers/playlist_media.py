from fastapi import HTTPException, Depends, APIRouter, Header
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

from api import database
from api.helpers import crud
from api.helpers.crud import get_user_data_by_token
from api.models.playlist_media_model import PlaylistMedia
from api.models.playlist_model import Playlist
from api.schemas.playlist_media_schema import PlaylistMediaCreate, PlaylistMediaBase

router = APIRouter()


@router.post("/playlist/tracks/")
def add_tracks_to_playlist(
        playlist_media: PlaylistMediaCreate,
        authorization: str = Header(...),
        db_session: Session = Depends(database.get_db)
):
    """
    Add a media item to a playlist

    Args:
        playlist_media (PlaylistMediaCreate): Playlist media association data
        db (Session): Database session

    Returns:
        PlaylistMediaResponse: Created playlist media association
    """

    try:
        user_email_data = get_user_data_by_token(authorization)
        if not user_email_data:
            raise HTTPException(status_code=404, detail="Invalid authorization token")

        db_playlist_media = PlaylistMedia(
            playlist_id=playlist_media.playlist_id,
            media_id=playlist_media.media_id
        )

        db_session.add(db_playlist_media)
        db_session.commit()
        db_session.refresh(db_playlist_media)
        return {"message": "Media added successfully to Playlist"}

    except IntegrityError as integrity_error:
        db_session.rollback()
        raise HTTPException(status_code=400, detail="Unable to add media to playlist.")

    except HTTPException as http_exc:
        db_session.rollback()
        raise http_exc

    except Exception as exec:
        db_session.rollback()
        raise HTTPException(status_code=500, detail="An unexpected error occurred. Please try again later.")


@router.get("/playlist/tracks/")
def get_playlist_tracks(
        playlist_id: int,
        authorization: str = Header(...),
        db_session: Session = Depends(database.get_db)
):
    """
    Retrieve a playlist with its tracks

    Args:
        playlist_id (int): ID of the playlist to retrieve
        authorization (str): User authorization token
        db_session (Session): Database session

    Returns:
        Dict: Playlist details with associated tracks
    """
    try:
        user_email_data = get_user_data_by_token(authorization)
        if not user_email_data:
            raise HTTPException(status_code=404, detail="Invalid authorization token")

        db_user = crud.get_user_by_email(db_session, email=user_email_data)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        playlist = (
            db_session.query(Playlist)
            .filter_by(playlist_id=playlist_id, user_id=db_user.user_id)
            .options(
                joinedload(Playlist.playlist_media).joinedload(PlaylistMedia.media)
            )
            .first()
        )

        if not playlist:
            raise HTTPException(
                status_code=404,
                detail="Playlist not found or you do not have access to this playlist"
            )

            # Transform playlist to a dictionary with tracks
        playlist_data = {
            "playlist_id": playlist.playlist_id,
            "playlist_title": playlist.playlist_title,
            "description": playlist.description,
            "is_public": playlist.is_public,
            "tracks": []
        }

        # Extract track information
        for playlist_media in playlist.playlist_media:
            media = playlist_media.media
            track_info = {
                "media_id": media.media_id,
                "title": media.media_title,  # Adjust based on your Media model
                "thumbnail_image": media.thumbnail_image_path,  # Adjust based on your Media model
                "s3_media_path": media.s3_media_path,  # Adjust based on your Media model
            }
            playlist_data["tracks"].append(track_info)

        return {
            "message": "Playlist retrieved successfully",
            "data": playlist_data
        }

    except IntegrityError:
        db_session.rollback()
        raise HTTPException(status_code=400, detail="Database integrity error")

    except HTTPException as http_exc:
        db_session.rollback()
        raise http_exc

    except Exception as exec:
        db_session.rollback()
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred. Please try again later."
        )


@router.delete("/playlist/tracks/")
def remove_track_from_playlist(
        playlist_track_remove: PlaylistMediaBase,
        authorization: str = Header(...),
        db_session: Session = Depends(database.get_db)
):
    """
    Remove a track from a playlist

    Args:
        playlist_track_remove (PlaylistTrackRemove): Details of track to remove from playlist
        authorization (str): User authorization token
        db_session (Session): Database session

    Returns:
        dict: Confirmation message of track removal
    """
    try:
        # Validate user authorization
        user_email_data = get_user_data_by_token(authorization)
        if not user_email_data:
            raise HTTPException(status_code=401, detail="Invalid authorization token")

        db_user = crud.get_user_by_email(db_session, email=user_email_data)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        # Verify playlist ownership
        playlist = db_session.query(Playlist).filter(
            Playlist.playlist_id == playlist_track_remove.playlist_id,
            Playlist.user_id == db_user.user_id
        ).first()

        if not playlist:
            raise HTTPException(
                status_code=404,
                detail="Playlist not found or you do not have permission to modify it"
            )

        # Find the track in the playlist
        playlist_track = db_session.query(PlaylistMedia).filter(
            PlaylistMedia.playlist_id == playlist_track_remove.playlist_id,
            PlaylistMedia.media_id == playlist_track_remove.media_id
        ).first()

        if not playlist_track:
            raise HTTPException(
                status_code=404,
                detail="Track not found in the specified playlist"
            )

        # Remove the track from the playlist
        db_session.delete(playlist_track)
        db_session.commit()

        return {
            "message": "Track successfully removed from playlist",
            "playlist_id": playlist_track_remove.playlist_id,
            "media_id": playlist_track_remove.media_id
        }

    except IntegrityError:
        db_session.rollback()
        raise HTTPException(
            status_code=400,
            detail="Unable to remove track from playlist due to database constraint"
        )

    except HTTPException as http_exc:
        db_session.rollback()
        raise http_exc

    except Exception as exc:
        db_session.rollback()
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while removing track from playlist"
        )
