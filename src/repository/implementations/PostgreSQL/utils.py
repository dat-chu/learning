from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.exceptions import BaseAppException
from src.repository.implementations.PostgreSQL.models.index import User, Course
from typing import Optional

async def get_user_by_username(db: Optional[AsyncSession], username: str) -> Optional[User]:
    if db is None:
        raise BaseAppException("Database session is not initialized")
    result = await db.execute(select(User).where(User.username == username))
    return result.scalars().first()

async def get_user_by_id(db: Optional[AsyncSession], user_id: int) -> Optional[User]:
    if db is None:
        raise BaseAppException("Database session is not initialized")
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalars().first()

async def get_course_by_id(db: Optional[AsyncSession], course_id: int):
    if db is None:
        raise BaseAppException("Database session is not initialized")
    result = await db.execute(select(Course).where(Course.id == course_id))
    return result.scalars().first()