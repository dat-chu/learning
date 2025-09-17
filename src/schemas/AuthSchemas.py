from pydantic import BaseModel

class UserSignupRequest(BaseModel):
    username: str
    password: str
    role: str

class UserLoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"