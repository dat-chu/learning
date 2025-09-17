from src.exceptions import BaseAppException, UserAlreadyExistsException
from src.repository.interfaces.interface_AuthRepository import AuthRepository as AuthRepositoryInterface
from src.schemas import UserSchemas, AuthSchemas
import logging

logger = logging.getLogger(__name__)

class AuthService:

    def __init__(self, auth_repository: AuthRepositoryInterface):
        self.auth_repository = auth_repository

    async def signup(self, user_instance: AuthSchemas.UserSignupRequest) -> UserSchemas.UserResponse:
        try:
            user = await self.auth_repository.signup(user_instance)
            return UserSchemas.UserResponse(
                id=user.id,
                username=user.username,
                role=user.role,
                created_at=user.created_at
            )
        except UserAlreadyExistsException:
            raise 
        except Exception as e:
            logger.exception(f"Error getting user: {str(e)}")
            raise BaseAppException(f"Error getting user: {str(e)}") from e
        
    async def login(self, login_data: AuthSchemas.UserLoginRequest) -> str:
        try:
            token = await self.auth_repository.login(login_data)
            return AuthSchemas.LoginResponse(access_token=token)
        except Exception as e:
            logger.exception(f"Error during login: {str(e)}")
            raise BaseAppException(f"Error during login: {str(e)}") from e