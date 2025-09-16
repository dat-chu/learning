from sqlalchemy.ext.asyncio import AsyncSession
from src.repository.interfaces.interface_UserRepository import UserRepository as UserRepositoryInterface
from src.repository.implementations.PostgreSQL.postgres_UserRepository import UserRepository as PostgresUserRepository
from .settings import get_settings, DatabaseType

def create_user_repository(db_context: AsyncSession) -> UserRepositoryInterface:
    """
    Creates the appropriate repository based on configuration.
    For PostgreSQL: Uses the provided database session
    """
    settings = get_settings()

    if settings.DATABASE_TYPE == DatabaseType.POSTGRES:
        return PostgresUserRepository(db_context)
    else:
        raise ValueError(f"Unsupported database type: {settings.DATABASE_TYPE}")