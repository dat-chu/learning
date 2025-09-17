from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class ProgressBase(BaseModel):
    user_id: int
    lesson_id: int
    completed: bool = False

class ProgressCreateRequest(ProgressBase):
    pass

class ProgressUpdateRequest(BaseModel):
    completed: bool

class ProgressResponse(ProgressBase):
    id: int
    completed_at: Optional[datetime]
    model_config = ConfigDict(from_attributes=True)