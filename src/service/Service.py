from src.exceptions import BaseAppException, ResourceNotFoundException
from src.repository.interfaces.interface_Repository import Repository as RepositoryInterface
from src.schemas import UserSchemas
import logging

logger = logging.getLogger(__name__)

class Service:

    def __init__(self, repository: RepositoryInterface):
        self.repository = repository

    async def get_user(self, email: str) -> UserSchemas.UserResponse:
        try:
            user = await self.repository.get_user(email)
            return UserSchemas.UserResponse(
                email=user.email,
                is_active=user.is_active
            )
        except ResourceNotFoundException:
            raise #Re-raise from repository layer
        except Exception as e:
            logger.exception(f"Error getting user: {str(e)}")
            raise BaseAppException(f"Error getting user: {str(e)}") from e

    async def create_user(
        self,
        email: str
    ) -> UserSchemas.UserResponse:

        user = await self.repository.create_user(
            User_instance = UserSchemas.User(
                email=email
            )
        )
        return UserSchemas.UserResponse(
            email=user.email,
            is_active=user.is_active
        )