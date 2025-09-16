from src.exceptions import BaseAppException, ResourceNotFoundException
from src.repository.interfaces.interface_UserRepository import UserRepository as UserRepositoryInterface
from src.schemas import UserSchemas
import logging

logger = logging.getLogger(__name__)

class UserService:

    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository

    async def get_user(self, username: str) -> UserSchemas.UserResponse:
        try:
            user = await self.user_repository.get_user(username)
            return UserSchemas.UserResponse(
                id=user.id,
                username=user.username,
                role=user.role,
                created_at=user.created_at
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

        pass