from src.exceptions import BaseAppException, ResourceNotFoundException, UserAlreadyExistsException
from src.repository.interfaces import interface_UserRepository
from src.schemas import UserSchemas
import logging
from src.repository.implementations.PostgreSQL.models.index import User
from src.repository.implementations.PostgreSQL.utils import get_user_by_username, get_user_by_id
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

logger = logging.getLogger(__name__)

class UserRepository(interface_UserRepository.UserRepository):

    def __init__(self, db = None):
        self.db = db

    async def get_user(
        self,
        username: str,
    ) -> User:
        try:
            user = await get_user_by_username(self.db, username)
            if user is None:
                logger.warning(f"User with {username} not found")
                raise ResourceNotFoundException(f"User with {username} not found")

            return user

        # Catch the ResourceNotFoundException and raise to other layers
        except ResourceNotFoundException:
            raise

        # Catch the Uncaught exception and raise to other layers as BaseAppException
        except Exception as e:
            logger.exception(f"Error getting user: {str(e)}")
            raise BaseAppException(f"Internal database error: {str(e)}") from e


    async def create_user(
        self,
        user_instance: UserSchemas.UserCreateRequest
    ) -> User:
        if self.db is None:
            raise BaseAppException("Database session is not initialized")
        try:
            existing_user = self.get_user(user_instance.username)
            if existing_user:
                raise UserAlreadyExistsException("User already exists")

            hashed_password = pwd_context.hash(user_instance.password)

            new_user = User(
                username=user_instance.username,
                password_hash=hashed_password,
                role=user_instance.role or "user"
            )

            self.db.add(new_user)
            await self.db.commit()
            await self.db.refresh(new_user)

            return new_user

        except (UserAlreadyExistsException, ResourceNotFoundException):
            raise

        except Exception as e:
            logger.exception(f"Error creating user: {str(e)}")
            raise BaseAppException(f"Internal database error: {str(e)}") from e


    async def update_user(self, user_id: int, update_data: UserSchemas.UserUpdateRequest) -> User:
        try:
            user = await get_user_by_id(self.db, user_id)

            if not user:
                raise ResourceNotFoundException(f"User with id={user_id} not found")

            if update_data.username and update_data.username != user.username:
                existing = await get_user_by_username(self.db, update_data.username)
                if existing:
                    raise UserAlreadyExistsException("Username already exists")
                user.username = update_data.username

            # Update password nếu có
            if update_data.password:
                user.password_hash = pwd_context.hash(update_data.password)

            # Update role nếu có
            if update_data.role:
                user.role = update_data.role

            await self.db.commit()
            await self.db.refresh(user)
            return user

        except (ResourceNotFoundException, UserAlreadyExistsException):
            raise
        except Exception as e:
            await self.db.rollback()
            raise BaseAppException(f"Error updating user: {str(e)}") from e