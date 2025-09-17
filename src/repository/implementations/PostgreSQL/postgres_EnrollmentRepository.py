import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.repository.interfaces.interface_EnrollmentRepository import EnrollmentRepository as EnrollmentRepositoryInterface
from src.repository.implementations.PostgreSQL.models.index import Enrollment
from src.schemas import EnrollmentSchemas
from src.exceptions import BaseAppException, ResourceNotFoundException

logger = logging.getLogger(__name__)

class EnrollmentRepository(EnrollmentRepositoryInterface):

    def __init__(self, db: AsyncSession):
        self.db = db

    async def enroll_user(self, enrollment: EnrollmentSchemas.EnrollmentCreateRequest) -> Enrollment:
        try:
            new_enrollment = Enrollment(
                user_id=enrollment.user_id,
                course_id=enrollment.course_id
            )
            self.db.add(new_enrollment)
            await self.db.commit()
            await self.db.refresh(new_enrollment)
            return new_enrollment
        except Exception as e:
            logger.exception(f"Error enrolling user: {str(e)}")
            await self.db.rollback()
            raise BaseAppException(f"Error enrolling user: {str(e)}") from e

    async def get_enrollments_by_user(self, user_id: int) -> list[Enrollment]:
        try:
            result = await self.db.execute(
                select(Enrollment).where(Enrollment.user_id == user_id)
            )
            return result.scalars().all()
        except Exception as e:
            logger.exception(f"Error fetching enrollments for user {user_id}: {str(e)}")
            raise BaseAppException(f"Error fetching enrollments for user {user_id}")

    async def get_enrollments_by_course(self, course_id: int) -> list[Enrollment]:
        try:
            result = await self.db.execute(
                select(Enrollment).where(Enrollment.course_id == course_id)
            )
            return result.scalars().all()
        except Exception as e:
            logger.exception(f"Error fetching enrollments for course {course_id}: {str(e)}")
            raise BaseAppException(f"Error fetching enrollments for course {course_id}")

    async def remove_enrollment(self, enrollment_id: int) -> str:
        try:
            result = await self.db.execute(
                select(Enrollment).where(Enrollment.id == enrollment_id)
            )
            enrollment = result.scalar_one_or_none()
            if not enrollment:
                raise ResourceNotFoundException(f"Enrollment with id={enrollment_id} not found")

            await self.db.delete(enrollment)
            await self.db.commit()
            return f"Enrollment with id={enrollment_id} has been removed"
        except ResourceNotFoundException:
            raise
        except Exception as e:
            logger.exception(f"Error removing enrollment {enrollment_id}: {str(e)}")
            await self.db.rollback()
            raise BaseAppException(f"Error removing enrollment {enrollment_id}")
