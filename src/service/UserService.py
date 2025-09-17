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
            return UserSchemas.UserResponse.model_validate(user)
        except ResourceNotFoundException:
            raise #Re-raise from repository layer
        except Exception as e:
            logger.exception(f"Error getting user: {str(e)}")
            raise BaseAppException(f"Error getting user: {str(e)}") from e

    async def create_user(
        self,
        user_instance: UserSchemas.UserCreateRequest
    ) -> UserSchemas.UserResponse:
        new_user = await self.user_repository.create_user(user_instance)
        return UserSchemas.UserResponse.model_validate(new_user)

    async def update_user(
        self,
        user_instance: UserSchemas.UserUpdateRequest
    ) -> UserSchemas.UserResponse:
        updated_user = await self.user_repository.update_user(user_instance)
        return UserSchemas.UserResponse.model_validate(updated_user)
