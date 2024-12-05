import requests
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session

from api import database
from api.models.album_model import Album
from api.models.artist_model import Artist
from api.models.media_model import Media

router = APIRouter()


@router.get("/search")
def search_entities(query: str, db: Session = Depends(database.get_db)):
    """
    Search for data in Media, Album, and Artist tables based on a query string.

    Args:
        query (str): Search query to match against media title, album title, or artist name.
        db (Session): Database session.

    Returns:
        dict: JSON response with matched media, albums, and artists.
    """
    try:
        # Search Media
        media_results = db.query(Media).filter(
            Media.media_title.ilike(f"%{query}%")
        ).all()

        # Search Albums
        album_results = db.query(Album).filter(
            Album.album_title.ilike(f"%{query}%")
        ).all()

        # Search Artists
        artist_results = db.query(Artist).filter(
            Artist.artist_name.ilike(f"%{query}%")
        ).all()

        # Format the results
        media_list = [
            {
                "id": media.media_id,
                "title": media.media_title,
                "duration": media.duration,
                "thumbnail": media.thumbnail_image_path,
                "views": media.view_count,
            }
            for media in media_results
        ]

        album_list = [
            {
                "id": album.album_id,
                "title": album.album_title,
                "release_date": album.release_date.strftime("%Y-%m-%d"),
                "cover_art": album.cover_art,
            }
            for album in album_results
        ]

        artist_list = [
            {
                "id": artist.artist_id,
                "name": artist.artist_name,
                "profile_picture": artist.profile_picture,
            }
            for artist in artist_results
        ]

        return {
            "tracks": media_list,
            "albums": album_list,
            "artists": artist_list,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


SPOTIFY_SEARCH_API_URL = "https://api.spotify.com/v1/search"


@router.get("/spotify-search")
async def search_spotify(
        q: str,
        type: str = "track",
        limit: int = 10,
        offset: int = 0,
        authorization: str = Header(...)
):
    """
    Search the Spotify API.
    Args:
        q (str): Search query
        type (str): The type of search (default: "track,album")
        limit (int): Number of results to limit to (default: 5)
        offset (int): Number of results to skip (default: 0)
        authorization (str): Bearer token for Spotify API
    """
    headers = {"Authorization": f"Bearer {authorization}"}
    params = {"q": q, "type": type, "limit": limit}

    try:
        response = requests.get(SPOTIFY_SEARCH_API_URL, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        raise HTTPException(status_code=response.status_code, detail=response.text) from e


SPOTIFY_TRACK_API = "https://api.spotify.com/v1/tracks/"

@router.get("/track/{track_id}")
def get_track_info(track_id: str, authorization: str = Header(...)):
    """
    Fetch detailed information about a specific track from Spotify.

    Args:
        track_id (str): Spotify Track ID.
        authorization (str): Bearer token for Spotify API.

    Returns:
        dict: Track information from Spotify API.
    """
    headers = {"Authorization": f"Bearer {authorization}"}

    try:
        # Make a GET request to the Spotify API
        response = requests.get(f"{SPOTIFY_TRACK_API}{track_id}", headers=headers)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.HTTPError as e:
        if response.status_code == 401:
            raise HTTPException(status_code=401, detail="Unauthorized. Check your access token.")
        elif response.status_code == 404:
            raise HTTPException(status_code=404, detail="Track not found.")
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")