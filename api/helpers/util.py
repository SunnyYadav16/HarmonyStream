from datetime import datetime, timedelta

from fastapi import HTTPException
from jose import jwt, JWTError
from passlib.context import CryptContext

SECRET_KEY = "VERY-SECRET-KEY"  # Secure random secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Verify password function
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# Hash password function
def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data):
    """
    Create an access token with an expiration time

    Args:
        data (dict): Payload data to be encoded in the token

    Returns:
        str: Encoded JWT token
    """
    # Create a dictionary with necessary user information
    to_encode = {
        "sub": data.email,  # Use email as the subject
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }

    # Set expiration
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    # Encode token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict):
    """
    Create a refresh token with a longer expiration time

    Args:
        data (dict): Payload data to be encoded in the token

    Returns:
        str: Encoded refresh JWT token
    """
    to_encode = data.copy()

    # Set longer expiration for refresh token
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})

    # Encode token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str):
    """
    Verify and decode a JWT token

    Args:
        token (str): JWT token to verify

    Returns:
        dict: Decoded token payload

    Raises:
        JWTError: If token is invalid or expired
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        return email
    except JWTError:
        raise HTTPException(status_code=500, detail="Could not validate token")
