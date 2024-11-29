from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict

class CommentBase(BaseModel):
    user_id: int
    media_id: int
    comment_text: str = Field(..., min_length=1)

class CommentCreate(CommentBase):
    pass

class CommentResponse(CommentBase):
    comment_id: int
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)