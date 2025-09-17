from abc import ABC, abstractmethod
from src.schemas import UserSchemas
from src.repository.implementations.PostgreSQL.models.index import User

class UserRepository(ABC):

    @abstractmethod
    async def get_user(self, username: str) -> User:
        pass

    @abstractmethod
    async def create_user(self, user_instance: UserSchemas.UserCreateRequest) -> User:
        pass

    @abstractmethod
    async def update_user(self, user_instance: UserSchemas.UserUpdateRequest) -> User:
        pass