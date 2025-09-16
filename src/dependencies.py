from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.repository.interfaces.interface_UserRepository import UserRepository as UserRepositoryInterface
from src.service.UserService import UserService
from src.db.factory import create_user_repository
from src.db.db_context import db_context

async def get_user_repository(db: AsyncSession = Depends(db_context)) -> UserRepositoryInterface:
    return create_user_repository(db)

async def get_user_service(repository: UserRepositoryInterface = Depends(get_user_repository)) -> UserService:
    return UserService(repository)