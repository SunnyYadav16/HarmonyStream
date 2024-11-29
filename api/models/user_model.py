"""User model."""
#--------------------------------------------#
# PEP-8 Imports Priority.
# 1.Standard Library Imports
# 2.Related Library Imports
# 3.Local application/library imports
#--------------------------------------------#
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, Boolean
from sqlalchemy.orm import relationship
from api.database import Base
from api.models.role_model import RoleResponse
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr, ConfigDict


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    username = Column(String(255), unique=True, nullable=False)
    email = Column(String(320), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    profile_picture = Column(String(255), nullable=True)
    user_role = Column(Integer, ForeignKey('roles.role_id'), default=1)
    last_login = Column(DateTime, server_default=func.now(), onupdate=func.now())
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime, nullable=True)
    is_premium = Column(Boolean, default=False)

    # Relationship to role
    role = relationship("Role", back_populates="users")


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
