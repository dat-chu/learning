from typing import Self
from pydantic import BaseModel, model_validator

class UserSignupRequest(BaseModel):
    username: str
    password: str
    password_repeat: str
    role: str

    @model_validator(mode='after')
    def check_passwords_match(self) -> Self:
        if self.password != self.password_repeat:
            raise ValueError('Passwords do not match')
        return self

class UserLoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"