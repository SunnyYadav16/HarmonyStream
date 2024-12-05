from fastapi import HTTPException, Depends, APIRouter, Header
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from api import database
from api.helpers import crud
from api.helpers.crud import get_user_data_by_token
from api.models.playlist_media_model import PlaylistMedia
from api.models.playlist_model import Playlist
from api.schemas.playlist_schema import PlaylistResponse, PlaylistCreate

router = APIRouter()


@router.post("/playlist/")
def create_playlist(
        playlist: PlaylistCreate,
        authorization: str = Header(...),
        db_session: Session = Depends(database.get_db)
):
    """
    Create a new playlist

    Args:
        playlist (PlaylistCreate): Playlist creation data
        db (Session): Database session

    Returns:
        PlaylistResponse: Created playlist details
    """

    try:
        user_email_data = get_user_data_by_token(authorization)
        if not user_email_data:
            raise HTTPException(status_code=404, detail="Invalid authorization token")

        db_user = crud.get_user_by_email(db_session, email=user_email_data)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        db_playlist = Playlist(
            user_id=db_user.user_id,
            playlist_title=playlist.playlist_title,
            description=playlist.description,
            is_public=playlist.is_public or False
        )

        db_session.add(db_playlist)
        db_session.commit()
        db_session.refresh(db_playlist)
        return {"message": "Playlist created successfully"}

    except IntegrityError as integrity_error:
        db_session.rollback()
        raise HTTPException(status_code=400, detail="Unable to make playlist due to database integrity constraints.")

    except HTTPException as http_exc:
        db_session.rollback()
        raise http_exc

    except Exception as exec:
        db_session.rollback()
        raise HTTPException(status_code=500, detail="An unexpected error occurred. Please try again later.")


@router.get("/playlist/")
def get_user_playlists(authorization: str = Header(...), db_session: Session = Depends(database.get_db)):
    """
    Retrieve all playlists for a specific user.

    - **user_id**: The ID of the user whose playlists are to be retrieved
    - Returns a list of playlists with their tracks
    """
    try:
        user_email_data = get_user_data_by_token(authorization)
        if not user_email_data:
            raise HTTPException(status_code=404, detail="Invalid authorization token")

        db_user = crud.get_user_by_email(db_session, email=user_email_data)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        # Retrieve playlists with tracks
        playlists = db_session.query(Playlist.playlist_id, Playlist.playlist_title, Playlist.description,
                                     Playlist.is_public, Playlist.created_at).filter(
            Playlist.user_id == db_user.user_id).all()

        playlists_data = {
            "playlists": playlists
        }
        return playlists_data

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


@router.delete("/playlist/", response_model=dict)
def delete_playlist(
        playlist_id: int,
        authorization: str = Header(...),
        db_session: Session = Depends(database.get_db)
):
    """
    Delete a playlist and all its associated tracks

    Args:
        playlist_id (int): ID of the playlist to delete
        authorization (str): User authorization token
        db_session (Session): Database session

    Returns:
        dict: Confirmation message of playlist deletion
    """
    try:
        # Validate user authorization
        user_email_data = get_user_data_by_token(authorization)
        if not user_email_data:
            raise HTTPException(status_code=401, detail="Invalid authorization token")

        db_user = crud.get_user_by_email(db_session, email=user_email_data)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        # Find the playlist and verify ownership
        playlist = db_session.query(Playlist).filter(
            Playlist.playlist_id == playlist_id,
            Playlist.user_id == db_user.user_id
        ).first()

        if not playlist:
            raise HTTPException(
                status_code=404,
                detail="Playlist not found or you do not have permission to delete it"
            )

        # Count tracks before deletion for response
        track_count = db_session.query(PlaylistMedia).filter(
            PlaylistMedia.playlist_id == playlist_id
        ).count()

        # Delete all associated tracks first
        db_session.query(PlaylistMedia).filter(
            PlaylistMedia.playlist_id == playlist_id
        ).delete(synchronize_session=False)

        # Delete the playlist
        db_session.delete(playlist)
        db_session.commit()

        return {
            "message": "Playlist deleted successfully",
            "playlist_id": playlist_id,
            "tracks_removed": track_count
        }

    except IntegrityError as integrity_error:
        db_session.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Database integrity error: {str(integrity_error)}"
        )

    except HTTPException as http_exc:
        db_session.rollback()
        raise http_exc

    except Exception as exc:
        db_session.rollback()
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while deleting the playlist"
        )
