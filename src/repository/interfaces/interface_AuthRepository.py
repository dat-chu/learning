from abc import ABC, abstractmethod
from src.schemas import AuthSchemas, UserSchemas

class AuthRepository(ABC):

    @abstractmethod
    async def signup(self, user_instance: AuthSchemas.UserSignupRequest) -> UserSchemas.User:
        """Sign up a new user"""
        pass

    @abstractmethod
    async def login(self, login_data: AuthSchemas.UserLoginRequest) -> str:
        """Log in a user and return a token"""
        pass