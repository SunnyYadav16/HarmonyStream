"""This module is for the users router."""
import random
import secrets

# --------------------------------------------#
# PEP-8 Imports Priority.
# 1.Standard Library Imports
# 2.Related Library Imports
# 3.Local application/library imports
# --------------------------------------------#
from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.orm import Session

from api.helpers import crud
from api.schemas import users_schema
from .. import database
from ..helpers.crud import get_user_data_by_token
from ..helpers.email import send_email
from ..helpers.util import create_access_token, get_password_hash, verify_password
from ..models.password_reset import PasswordReset
from ..schemas.password_reset_schema import PasswordResetSchema, PasswordRequestResetSchema

router = APIRouter()


@router.post("/users/")
def create_user(user: users_schema.UserCreate, db_session: Session = Depends(database.get_db)):
    """
    Create user router.
    :param user: The user schema.
    :param db_session: The database session.
    """
    db_user_email = crud.get_user_by_email(db_session, email=user.email)
    if db_user_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user_name = crud.get_user_by_username(db_session, username=user.username)
    if db_user_name:
        raise HTTPException(status_code=400, detail="Username already registered")

    user.password = get_password_hash(user.password)
    user_created = crud.create_user(db_session=db_session, user=user)
    if not user_created:
        raise HTTPException(status_code=500, detail="User creation failed")
    return {
        "message": "User created successfully.",
    }


@router.post("/user-login/", response_model=users_schema.Token)
def login_user(user: users_schema.UserLogin, db_session: Session = Depends(database.get_db)):
    """
    Login user router.
    :param user: The user login schema (contains email/username and password).
    :param db_session: The database session.
    """
    # Fetch user from database by email or username
    db_user = crud.get_user_by_email(db_session, user.email)
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Verify password
    if not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Username or password incorrect")

    # Generate JWT token
    access_token = create_access_token(db_user)
    if not access_token:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/get-user-profile/", response_model=users_schema.UserResponse)
def read_user(authorization: str = Header(...), db_session: Session = Depends(database.get_db)):
    """
    Get user by User ID router.
    :param authorization: The User ID.
    :param db_session: The database session.
    """
    user_email_data = get_user_data_by_token(authorization)

    db_user = crud.get_user_by_email(db_session, email=user_email_data)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    return db_user


@router.post("/request-password-reset/")
def request_password_reset(password_reset: PasswordRequestResetSchema, db_session: Session = Depends(database.get_db)):
    """
    Check if email exists and send OTP for password reset.
    """
    user_data = crud.get_user_by_email(db_session, email=password_reset.email)
    if not user_data:
        raise HTTPException(status_code=400, detail="User/Email not registered")

    # Generate 6-digit OTP
    otp = secrets.randbelow(900000) + 100000
    print(otp)

    # Store OTP in the database
    user_otp_data = crud.get_user_otp(db_session, user_data.user_id)
    if not user_otp_data:
        reset_request = PasswordReset(user_id=user_data.user_id, otp=str(otp))
        db_session.add(reset_request)
        db_session.commit()
    else:
        user_otp_data.user_id=user_data.user_id
        user_otp_data.otp=str(otp)
        db_session.commit()

    # Send OTP via email
    send_email(
        recipient_email=user_data.email,
        subject="Password Reset OTP",
        body=f"Your OTP for password reset is {otp}."
    )

    return {"message": "OTP sent to the registered email."}


@router.post("/reset-password/")
def reset_password(
        reset_password: PasswordResetSchema,
        db_session: Session = Depends(database.get_db)
):
    """
    Reset the password after OTP validation.
    """
    user = crud.get_user_by_email(db_session, email=reset_password.email)
    if not user:
        raise HTTPException(status_code=404, detail="User/Email not found")

    # Query the PasswordReset table for valid OTP
    reset_request = (
        db_session.query(PasswordReset)
        .filter(
            PasswordReset.user_id == user.user_id,
            PasswordReset.otp == reset_password.otp)
        .first()
    )

    if not reset_request:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")

    if verify_password(reset_password.new_password, user.password_hash):
        raise HTTPException(status_code=401, detail="Password cannot be same as previous passwords")

    if reset_password.new_password != reset_password.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    # Update password in database
    hashed_password = get_password_hash(reset_password.new_password)
    user.password_hash = hashed_password
    db_session.commit()

    # Optionally, delete OTP record to clean up
    db_session.query(PasswordReset).filter(PasswordReset.user_id == user.user_id).delete()
    db_session.commit()

    return {"message": "Password reset successful."}
