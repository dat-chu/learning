from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.repository.interfaces.interface_UserRepository import UserRepository as IUserRepo
from src.repository.interfaces.interface_AuthRepository import AuthRepository as IAuthRepo
from src.repository.interfaces.interface_CourseRepository import CourseRepository as ICourseRepo
from src.repository.interfaces.interface_LessonRepository import LessonRepository as ILessonRepo
from src.repository.interfaces.interface_EnrollmentRepository import EnrollmentRepository as IEnrollmentRepo
from src.service.UserService import UserService
from src.service.AuthService import AuthService
from src.service.CourseService import CourseService
from src.service.LessonService import LessonService
from src.service.EnrollmentService import EnrollmentService
from src.repository.interfaces.interface_ProgressRepository import ProgressRepository as IProgressRepo
from src.service.ProgressService import ProgressService
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

#LESSON
async def get_lesson_repository(db: AsyncSession = Depends(db_context)) -> ILessonRepo:
    return create_repository(db, repository_type="lesson")  # type: ignore

async def get_lesson_service(repo = Depends(get_lesson_repository)) -> LessonService:
    return LessonService(repo)

#ENROLLMENT
async def get_enrollment_repository(db: AsyncSession = Depends(db_context)) -> IEnrollmentRepo:
    return create_repository(db, repository_type="enrollment")  # type: ignore

async def get_enrollment_service(repo = Depends(get_enrollment_repository)) -> EnrollmentService:
    return EnrollmentService(repo)

# PROGRESS
async def get_progress_repository(db: AsyncSession = Depends(db_context)) -> IProgressRepo:
    return create_repository(db, repository_type="progress")  # type: ignore
async def get_progress_service(repo: IProgressRepo = Depends(get_progress_repository)) -> ProgressService:
    return ProgressService(repo)
