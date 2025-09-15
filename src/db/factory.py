from sqlalchemy.ext.asyncio import AsyncSession
from src.repository.interfaces.interface_Repository import Repository as RepositoryInterface
from src.repository.implementations.PostgreSQL.postgres_Repository import Repository as PostgresRepository
from .settings import get_settings, DatabaseType

def create_repository(db_context: AsyncSession) -> RepositoryInterface:
    """
    Creates the appropriate repository based on configuration.
    For PostgreSQL: Uses the provided database session
    """
    settings = get_settings()

    if settings.DATABASE_TYPE == DatabaseType.POSTGRES:
        return PostgresRepository(db_context)
    else:
        raise ValueError(f"Unsupported database type: {settings.DATABASE_TYPE}")