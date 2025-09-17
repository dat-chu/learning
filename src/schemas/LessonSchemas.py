from pydantic import BaseModel, ConfigDict
from typing import Optional


class LessonBase(BaseModel):
    course_id: int
    title: str
    content: Optional[str] = None
    video_url: Optional[str] = None
    order_index: Optional[int] = None


class LessonCreateRequest(LessonBase):
    pass


class LessonUpdateRequest(BaseModel):
    id: int
    title: Optional[str] = None
    content: Optional[str] = None
    video_url: Optional[str] = None
    order_index: Optional[int] = None


class LessonResponse(LessonBase):
    id: int
    model_config = ConfigDict(from_attributes=True)