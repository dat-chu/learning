from src.exceptions import BaseAppException, ResourceNotFoundException
from src.repository.interfaces import interface_UserRepository
from src.schemas import UserSchemas
import logging
from sqlalchemy.future import select
from src.repository.implementations.PostgreSQL.models.index import User

logger = logging.getLogger(__name__)

class UserRepository(interface_UserRepository.UserRepository):

    def __init__(self, db = None):
        self.db = db

    async def get_user(
        self,
        username: str,
    ) -> UserSchemas.User:
        try:
            result = await self.db.execute(select(User).where(User.username == username))
            user = result.scalars().first() 
            if user is None:
                logger.warning(f"User with {username} not found")
                raise ResourceNotFoundException(f"User with {username} not found")

            return UserSchemas.User(
                id=user.id,
                username=user.username,
                password_hash=user.password_hash,
                role=user.role,
                created_at=user.created_at,
            )

        # Catch the ResourceNotFoundException and raise to other layers
        except ResourceNotFoundException:
            raise

        # Catch the Uncaught exception and raise to other layers as BaseAppException
        except Exception as e:
            logger.exception(f"Error getting user: {str(e)}")
            raise BaseAppException(f"Internal database error: {str(e)}") from e



    async def create_user(
        self,
        User_instance: UserSchemas.User
    ) -> UserSchemas.User:

        pass


    async def update_user(
        self,
        User_instance: UserSchemas.User
    ) -> UserSchemas.User:

        pass