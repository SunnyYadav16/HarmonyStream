from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict

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