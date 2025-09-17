from abc import ABC, abstractmethod
from src.schemas import UserSchemas
from src.repository.implementations.PostgreSQL.models.index import User

class UserRepository(ABC):

    @abstractmethod
    async def get_user(self, username: str) -> User:
        """Get user by username"""
        pass

    @abstractmethod
    async def create_user(self, user_instance: UserSchemas.UserCreateRequest) -> User:
        """Create a new user"""
        pass

    @abstractmethod
    async def update_user(self, user_instance: UserSchemas.UserUpdateRequest) -> User:
        """Update an existing user"""
        pass