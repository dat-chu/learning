from typing import Callable, AsyncGenerator, Any
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.settings import get_settings, DatabaseType
from fastapi import Request


ContextDependency = Callable[..., AsyncGenerator[Any, None]]

def get_db_context() -> ContextDependency:
    """
    Returns the appropriate database context dependency based on configuration.
    For PostgreSQL: Returns a dependency that yields a database session
    """
    settings = get_settings()

    if settings.DATABASE_TYPE == DatabaseType.POSTGRES:
        # Return the PostgreSQL session dependency
        async def get_postgres_context(request: Request) -> AsyncGenerator[AsyncSession, None]:
            async_session_factory = request.app.state.postgres_session
            async with async_session_factory() as session:
                try:
                    yield session
                    await session.commit()  # Automatically commit if no exceptions
                except Exception:
                    await session.rollback()  # Rollback on exceptions
                    raise
        return get_postgres_context
    else:
        raise ValueError("Invalid DATABASE_TYPE")

# Create the context dependency based on current configuration
db_context = get_db_context()