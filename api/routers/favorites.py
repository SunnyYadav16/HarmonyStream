from fastapi import HTTPException, Depends, APIRouter, Header
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from api import database
from api.helpers import crud
from api.helpers.crud import get_user_data_by_token
from api.models.favorite_model import Favorite
from api.models.media_model import Media
from api.schemas import favorite_schema

router = APIRouter()


@router.post("/favorite/")
def favorite_song(favorite: favorite_schema.FavoriteCreate, authorization: str = Header(...),
                  db_session: Session = Depends(database.get_db)):
    """
    Mark a particular song as a favorite for a user.

    Args:
        favorite (favorite_schema.FavoriteCreate): The favorite schema containing user_id, media_id, and media_title.
        db_session (Session): The database session.

    Returns:
        dict: A message indicating the favorite operation's success or failure.
    """
    try:

        user_email_data = get_user_data_by_token(authorization)

        db_user = crud.get_user_by_email(db_session, email=user_email_data)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        # Check if the media exists
        media = db_session.query(Media).filter(
            Media.media_id == favorite.media_id,
            Media.media_title == favorite.media_title
        ).first()
        if not media:
            raise HTTPException(status_code=404,
                                detail=f"Media with ID {favorite.media_id} and title '{favorite.media_title}' not found.")

        # Check if the favorite already exists
        existing_favorite = db_session.query(Favorite).filter(
            Favorite.user_id == db_user.user_id,
            Favorite.media_id == favorite.media_id
        ).first()
        if existing_favorite:
            raise HTTPException(status_code=400, detail="Media is already marked as a favorite.")

        # Add to favorites
        new_favorite = Favorite(user_id=db_user.user_id, media_id=favorite.media_id)
        db_session.add(new_favorite)
        db_session.commit()

        return {"message": f"Media '{favorite.media_title}' has been marked as favorite."}

    except IntegrityError as integrity_error:
        db_session.rollback()
        raise HTTPException(status_code=400, detail="Unable to mark as favorite due to database integrity constraints.")

    except HTTPException as http_exc:
        raise http_exc

    except Exception as exec:
        db_session.rollback()
        raise HTTPException(status_code=500, detail="An unexpected error occurred. Please try again later.")


@router.get("/favorites/")
def get_user_favorites(authorization: str = Header(...), db_session: Session = Depends(database.get_db)):
    """
    Retrieve all favorite songs for a specific user.

    Args:
        user_id (int): The ID of the user.
        db_session (Session): Database session.

    Returns:
        dict: A list of favorite songs for the user.
    """
    try:

        user_email_data = get_user_data_by_token(authorization)

        db_user = crud.get_user_by_email(db_session, email=user_email_data)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        # Query the Favorite table and join with the Media table to get media details
        favorites = db_session.query(Favorite, Media).join(Media, Favorite.media_id == Media.media_id).filter(
            Favorite.user_id == db_user.user_id
        ).all()

        if not favorites:
            return {"favorites": []}
            # raise HTTPException(status_code=404, detail="No favorites found for the user.")

        # Format the results
        result = [
            {
                "media_id": media.media_id,
                "media_title": media.media_title,
                "thumbnail": media.thumbnail_image_path,
                "duration": media.duration,
                "views": media.view_count,
            }
            for favorite, media in favorites
        ]

        return {"favorites": result}

    except Exception as e:
        print(f"Unexpected Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")


@router.delete("/favorites/")
def delete_favorite(media_id: int, authorization: str = Header(...), db_session: Session = Depends(database.get_db)):
    """
    Delete a media item from a user's favorites.

    Args:
        user_id (int): The ID of the user.
        media_id (int): The ID of the media to delete.
        db_session (Session): Database session.

    Returns:
        dict: A message indicating success or failure.
    """
    try:
        user_email_data = get_user_data_by_token(authorization)

        db_user = crud.get_user_by_email(db_session, email=user_email_data)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        # Check if the media exists
        media = db_session.query(Media).filter(
            Media.media_id == media_id
        ).first()
        if not media:
            return {"message": "Media not found."}

        # Find the favorite entry
        favorite = db_session.query(Favorite).filter(
            Favorite.user_id == db_user.user_id,
            Favorite.media_id == media_id
        ).first()

        if not favorite:
            return {"message": "Media not found in user's favorites."}

        # Delete the favorite entry
        db_session.delete(favorite)
        db_session.commit()

        return {"message": f"Media with ID {media_id} has been removed from favorites."}

    except HTTPException as e:
        db_session.rollback()
        print(f"Unexpected Error:", e)
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )
