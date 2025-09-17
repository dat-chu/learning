import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from src.repository.interfaces.interface_ProgressRepository import ProgressRepository as ProgressRepositoryInterface
from src.repository.implementations.PostgreSQL.models.index import Progress, Lesson
from src.schemas import ProgressSchemas
from src.exceptions import BaseAppException, ResourceNotFoundException
from datetime import datetime

logger = logging.getLogger(__name__)

class ProgressRepository(ProgressRepositoryInterface):

    def __init__(self, db: AsyncSession):
        self.db = db

    async def mark_progress(self, progress: ProgressSchemas.ProgressCreateRequest) -> Progress:
        try:
            new_progress = Progress(
                user_id=progress.user_id,
                lesson_id=progress.lesson_id,
                completed=progress.completed,
                completed_at=datetime.utcnow() if progress.completed else None
            )
            self.db.add(new_progress)
            await self.db.commit()
            await self.db.refresh(new_progress)
            return new_progress
        except Exception as e:
            logger.exception(f"Error marking progress: {str(e)}")
            await self.db.rollback()
            raise BaseAppException(f"Error marking progress: {str(e)}") from e

    async def update_progress(self, progress_id: int, update: ProgressSchemas.ProgressUpdateRequest) -> Progress:
        try:
            result = await self.db.execute(select(Progress).where(Progress.id == progress_id))
            progress = result.scalar_one_or_none()
            if not progress:
                raise ResourceNotFoundException(f"Progress with id={progress_id} not found")

            progress.completed = update.completed
            progress.completed_at = datetime.utcnow() if update.completed else None

            await self.db.commit()
            await self.db.refresh(progress)
            return progress
        except ResourceNotFoundException:
            raise
        except Exception as e:
            logger.exception(f"Error updating progress: {str(e)}")
            await self.db.rollback()
            raise BaseAppException(f"Error updating progress: {str(e)}") from e

    async def get_user_progress_in_course(self, user_id: int, course_id: int) -> float:
        try:
            total_lessons_query = await self.db.execute(
                select(func.count(Lesson.id)).where(Lesson.course_id == course_id)
            )
            total_lessons = total_lessons_query.scalar_one()

            if total_lessons == 0:
                return 0.0

            completed_lessons_query = await self.db.execute(
                select(func.count(Progress.id))
                .join(Lesson, Lesson.id == Progress.lesson_id)
                .where(
                    Progress.user_id == user_id,
                    Lesson.course_id == course_id,
                    Progress.completed == True
                )
            )
            completed_lessons = completed_lessons_query.scalar_one()

            return (completed_lessons / total_lessons) * 100
        except Exception as e:
            logger.exception(f"Error calculating progress: {str(e)}")
            raise BaseAppException(f"Error calculating progress: {str(e)}")
