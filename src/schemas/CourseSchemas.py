from pydantic import BaseModel, ConfigDict
from typing import Optional

class CourseCreateRequest(BaseModel):
    title: str
    description: Optional[str] = None

class CourseUpdateRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class CourseResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    model_config = ConfigDict(from_attributes=True)
