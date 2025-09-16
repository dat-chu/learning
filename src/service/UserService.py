from src.exceptions import BaseAppException, ResourceNotFoundException
from src.repository.interfaces.interface_UserRepository import UserRepository as UserRepositoryInterface
from src.schemas import UserSchemas
import logging

logger = logging.getLogger(__name__)

class UserService:

    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository

    async def get_user(self, email: str) -> UserSchemas.UserResponse:
        try:
            user = await self.user_repository.get_user(email)
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

        user = await self.user_repository.create_user(
            User_instance = UserSchemas.User(
                email=email
            )
        )
        return UserSchemas.UserResponse(
            email=user.email,
            is_active=user.is_active
        )