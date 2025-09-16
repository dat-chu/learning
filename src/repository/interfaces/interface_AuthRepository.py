from abc import ABC, abstractmethod
from src.schemas import AuthSchemas, UserSchemas

class AuthRepository(ABC):

    @abstractmethod
    async def signup(self, user_instance: AuthSchemas.UserSignupRequest) -> UserSchemas.User:
        pass