from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class EnrollmentBase(BaseModel):
    user_id: int
    course_id: int

class EnrollmentCreateRequest(EnrollmentBase):
    pass

class EnrollmentResponse(EnrollmentBase):
    id: int
    enrolled_at: Optional[datetime]
    model_config = ConfigDict(from_attributes=True)