"""Pydantic schemas."""
# --------------------------------------------#
# PEP-8 Imports Priority.
# 1.Standard Library Imports
# 2.Related Library Imports
# 3.Local application/library imports
# --------------------------------------------#
from typing import Optional

from pydantic import BaseModel, Field, EmailStr, ConfigDict

from api.schemas.role_schema import RoleResponse


class UserBase(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=255)
    last_name: str = Field(..., min_length=2, max_length=255)
    username: str = Field(..., min_length=3, max_length=255)
    email: EmailStr
    profile_picture: Optional[str] = None
    user_role: Optional[int] = 1
    is_premium: Optional[bool] = False


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserLogin(BaseModel):
    email : EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class UserResponse(BaseModel):
    first_name: str
    last_name: str
    username : str
    email: EmailStr
    profile_picture : Optional[str] = None
    is_premium : Optional[bool] = False

    class Config:
        orm_mode = True

# Optional: Full User Details for Admin or Profile View
class UserDetailResponse(UserResponse):
    role: RoleResponse

    model_config = ConfigDict(from_attributes=True)
