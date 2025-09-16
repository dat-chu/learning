from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    id: Optional[int]
    username: str
    password_hash: str
    role: str = None
    created_at: datetime

class UserResponse(BaseModel):
    id: int
    username: str
    role: str = None
    created_at: datetime