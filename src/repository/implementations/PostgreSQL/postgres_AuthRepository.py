from src.repository.implementations.PostgreSQL.utils import get_user_by_username
from src.repository.interfaces.interface_AuthRepository import AuthRepository as AuthRepositoryInterface
import logging
from src.exceptions import BaseAppException, UserAlreadyExistsException
from src.schemas import AuthSchemas
from passlib.context import CryptContext
from src.repository.implementations.PostgreSQL.models.index import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

logger = logging.getLogger(__name__)

class AuthRepository(AuthRepositoryInterface):
    def __init__(self, db = None):
        self.db = db

    async def signup(self, user_instance: AuthSchemas.UserSignupRequest) -> str:
        try:
            username = user_instance.username
            password = user_instance.password
            role = user_instance.role

            existing_user = await get_user_by_username(self.db, username)
            if existing_user:
                raise UserAlreadyExistsException("User already exists")

            # Hash password
            hashed_password = pwd_context.hash(password)

            new_user = User(
                username=username,
                password_hash=hashed_password,
                role=role
            )

            self.db.add(new_user)
            await self.db.commit()
            await self.db.refresh(new_user)
            return new_user
        except Exception as e:
            logger.exception(f"Error creating user: {str(e)}")
            raise BaseAppException(f"Internal database error: {str(e)}") from e