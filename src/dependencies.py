from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.repository.interfaces.interface_Repository import Repository as RepositoryInterface
from src.service.Service import Service
from src.db.factory import create_repository
from src.db.db_context import db_context

async def get_repository(db: AsyncSession = Depends(db_context)) -> RepositoryInterface:
    return create_repository(db)

async def get_service(repository: RepositoryInterface = Depends(get_repository)) -> Service:
    return Service(repository)