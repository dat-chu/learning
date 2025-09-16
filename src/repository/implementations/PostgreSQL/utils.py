from src.schemas import UserSchemas
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.repository.implementations.PostgreSQL.models.index import User

async def get_user_by_username(db: AsyncSession, username: str) -> UserSchemas.User:
    result = await db.execute(select(User).where(User.username == username))
    return result.scalars().first() 