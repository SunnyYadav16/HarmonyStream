from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict
from sqlalchemy import Column, Integer, String, DateTime, Text, func
from sqlalchemy.orm import relationship

from api.database import Base


# SQLAlchemy Models
class Role(Base):
    __tablename__ = "roles"

    role_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    role_name = Column(String(255), unique=True, nullable=False)
    role_description = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationship to users
    users = relationship("User", back_populates="role")

# Pydantic Models for Request/Response Validation
class RoleBase(BaseModel):
    role_name: str = Field(..., min_length=2, max_length=255)
    role_description: Optional[str] = None

class RoleCreate(RoleBase):
    pass

class RoleResponse(RoleBase):
    role_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
