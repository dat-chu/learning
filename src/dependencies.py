from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.repository.interfaces.interface_UserRepository import UserRepository as IUserRepo
from src.repository.interfaces.interface_AuthRepository import AuthRepository as IAuthRepo
from src.repository.interfaces.interface_CourseRepository import CourseRepository as ICourseRepo
from src.service.UserService import UserService
from src.service.AuthService import AuthService
from src.service.CourseService import CourseService
from src.db.factory import create_repository
from src.db.db_context import db_context


# USER
async def get_user_repository(db: AsyncSession = Depends(db_context)) -> IUserRepo:
    return create_repository(db, repository_type="user")  # type: ignore

async def get_user_service(repo: IUserRepo = Depends(get_user_repository)) -> UserService:
    return UserService(repo)


# AUTH
async def get_auth_repository(db: AsyncSession = Depends(db_context)) -> IAuthRepo:
    return create_repository(db, repository_type="auth")  # type: ignore

async def get_auth_service(repo: IAuthRepo = Depends(get_auth_repository)) -> AuthService:
    return AuthService(repo)

# COURSE
async def get_course_repository(db: AsyncSession = Depends(db_context)) -> ICourseRepo:
    return create_repository(db, repository_type="course")  # type: ignore

async def get_course_service(repo: ICourseRepo = Depends(get_course_repository)) -> CourseService:
    return CourseService(repo)
