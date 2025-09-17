from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from enum import Enum


class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"

class User(BaseModel):
    id: Optional[int]
    username: str
    password_hash: str
    role: UserRole = UserRole.USER
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class UserResponse(BaseModel):
    id: int
    username: str
    role: UserRole = UserRole.USER
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class UserCreateRequest(BaseModel):
    username: str
    password: str
    role: Optional[UserRole] = UserRole.USER
    model_config = ConfigDict(from_attributes=True)

class UserUpdateRequest(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None
