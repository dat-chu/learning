from typing import Union
from sqlalchemy.ext.asyncio import AsyncSession

from src.repository.interfaces.interface_UserRepository import UserRepository as IUserRepo
from src.repository.interfaces.interface_AuthRepository import AuthRepository as IAuthRepo
from src.repository.interfaces.interface_CourseRepository import CourseRepository as ICourseRepo
from src.repository.interfaces.interface_LessonRepository import LessonRepository as ILessonRepo
from src.repository.interfaces.interface_EnrollmentRepository import EnrollmentRepository as IEnrollmentRepo
from src.repository.interfaces.interface_ProgressRepository import ProgressRepository as IProgressRepo
from src.repository.implementations.PostgreSQL.postgres_UserRepository import UserRepository as PgUserRepo
from src.repository.implementations.PostgreSQL.postgres_AuthRepository import AuthRepository as PgAuthRepo
from src.repository.implementations.PostgreSQL.postgres_CourseRepository import CourseRepository as PgCourseRepo
from src.repository.implementations.PostgreSQL.postgres_LessonRepository import LessonRepository as PgLessonRepo
from src.repository.implementations.PostgreSQL.postgres_EnrollmentRepository import EnrollmentRepository as PgEnrollmentRepo
from src.repository.implementations.PostgreSQL.postgres_ProgressRepository import ProgressRepository as PgProgressRepo
from .settings import get_settings, DatabaseType


def create_repository(db: AsyncSession, repository_type: str) -> Union[IUserRepo, IAuthRepo, ICourseRepo, ILessonRepo, IEnrollmentRepo, IProgressRepo]:
    """
    Factory method to create repository based on type and DB backend.
    """
    settings = get_settings()

    if settings.DATABASE_TYPE == DatabaseType.POSTGRES:
        repo_map = {
            "user": PgUserRepo,
            "auth": PgAuthRepo,
            "course": PgCourseRepo,
            "lesson": PgLessonRepo,
            "enrollment": PgEnrollmentRepo,
            "progress": PgProgressRepo,
        }

        repo_class = repo_map.get(repository_type)
        if not repo_class:
            raise ValueError(f"Unsupported repository type: {repository_type}")

        return repo_class(db)
    else:
        raise ValueError(f"Unsupported database type: {settings.DATABASE_TYPE}")
