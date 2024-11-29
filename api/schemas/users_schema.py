"""Pydantic schemas."""
#--------------------------------------------#
# PEP-8 Imports Priority.
# 1.Standard Library Imports
# 2.Related Library Imports
# 3.Local application/library imports
#--------------------------------------------#
from datetime import datetime
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

class UserResponse(UserBase):
    user_id: int
    last_login: datetime
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)

# Optional: Full User Details for Admin or Profile View
class UserDetailResponse(UserResponse):
    role: RoleResponse

    model_config = ConfigDict(from_attributes=True)