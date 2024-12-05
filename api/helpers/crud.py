"""This module is the helper for all crud operations."""
# --------------------------------------------#
# PEP-8 Imports Priority.
# 1.Standard Library Imports
# 2.Related Library Imports
# 3.Local application/library imports
# --------------------------------------------#
from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from api.helpers.util import verify_token
from api.models import user_model
from api.models.password_reset import PasswordReset
from api.schemas import users_schema


def get_user(db_session: Session, user_id: int):
    """
    Get user by User ID helper.
    :param db_session: The database session.
    :param user_id: The User ID.
    """
    return db_session.query(user_model.User).filter(user_model.User.id == user_id).first()


def update_user(db_session: Session, user_id: int, user: users_schema.UserCreate):
    """
    Update user by User ID helper.
    :param db_session: The database session.
    :param user_id: The User ID.
    """
    user_obj = get_user(db_session=db_session, user_id=user_id)
    if user_obj:
        user_obj.email = user.email
        db_session.add(user_obj)
        db_session.commit()
    return user_obj


def delete_user(db_session: Session, user_id: int):
    """
    Delete user by User ID helper.
    :param db_session: The database session.
    :param user_id: The User ID.
    """
    user_obj = get_user(db_session=db_session, user_id=user_id)
    if user_obj:
        db_session.delete(user_obj)
        db_session.commit()
    return user_obj


def get_user_by_email(db_session: Session, email: str):
    """
    Get user by User email helper.
    :param db_session: The database session.
    :param email: The User Email.
    """
    return db_session.query(user_model.User).filter(user_model.User.email == email).first()


def get_user_data_by_token(authorization: str):
    try:
        token = authorization.split(" ")[1]  # Extract token after "Bearer"
    except IndexError:
        raise HTTPException(status_code=401, detail="Invalid Authorization header format")

    token_data = verify_token(token)
    if token_data is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    return token_data


def get_user_by_username(db_session: Session, username: str):
    """
        Get user by User username helper.
        :param db_session: The database session.
        :param username: The User Username.
        """
    return db_session.query(user_model.User).filter(user_model.User.username == username).first()


def get_users(db_session: Session, skip: int = 0, limit: int = 100) -> List:
    """
    Get all users helper.
    :param db_session: The database session.
    :param skip: The offset used when paging.
    :param limit: The number of users to retrieve per query.
    """
    return db_session.query(user_model.User).offset(skip).limit(limit).all()


def create_user(db_session: Session, user: users_schema.UserCreate):
    """
    Create user helper.
    :param db_session: The database session.
    :param user: The user schema.
    """
    db_user = user_model.User(
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        email=user.email,
        password_hash=user.password,
        profile_picture=user.profile_picture,
        user_role=user.user_role,
        is_premium=user.is_premium,
    )
    db_session.add(db_user)
    db_session.commit()
    db_session.refresh(db_user)
    return db_user

def get_user_otp(db_session: Session, user_id: int):
    """
    Get all items helper.
    :param db_session: The database session.
    :param skip: The offset used when paging.
    :param limit: The number of items to retrieve per query.
    """
    return db_session.query(PasswordReset).filter(PasswordReset.user_id == user_id).first()


def update_user_otp(db_session: Session, user_id: int, otp: str):
    reset_request = db_session.query(PasswordReset).filter(PasswordReset.user_id == user_id).update({"otp": otp})
    db_session.add(reset_request)
    db_session.commit()
    return