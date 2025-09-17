import logging

from sqlalchemy import select
from src.exceptions import BaseAppException, ResourceNotFoundException
from src.schemas import LessonSchemas
from src.repository.implementations.PostgreSQL.models.index import Lesson
from src.repository.implementations.PostgreSQL.utils import get_lesson_by_id
from typing import List, Optional

logger = logging.getLogger(__name__)

class LessonRepository:
    def __init__(self, db=None):
        self.db = db

    async def get_lesson(self, lesson_id: int) -> Optional[Lesson]:
        try:
            lesson = await get_lesson_by_id(self.db, lesson_id)
            if not lesson:
                raise ResourceNotFoundException(f"Lesson with id={lesson_id} not found")
            return lesson
        except ResourceNotFoundException:
            raise
        except Exception as e:
            logger.exception(f"Error getting lesson: {str(e)}")
            raise BaseAppException(f"Internal database error: {str(e)}") from e
        
    async def get_lessons_by_course(self, course_id: int) -> List[Lesson]:
        try:
            stmt = (
                select(Lesson)
                .where(Lesson.course_id == course_id)
                .order_by(Lesson.order_index.asc())
            )
            result = await self.db.execute(stmt)
            lessons = result.scalars().all()
            return lessons
        except Exception as e:
            logger.exception(f"Error getting lessons by course: {str(e)}")
            raise BaseAppException(f"Internal database error: {str(e)}") from e

    async def create_lesson(self, lesson_instance: LessonSchemas.LessonCreateRequest) -> Lesson:
        try:
            new_lesson = Lesson(
                course_id=lesson_instance.course_id,
                title=lesson_instance.title,
                content=lesson_instance.content,
                video_url=lesson_instance.video_url,
                order_index=lesson_instance.order_index,
            )
            self.db.add(new_lesson)
            await self.db.commit()
            await self.db.refresh(new_lesson)
            return new_lesson
        except Exception as e:
            logger.exception(f"Error creating lesson: {str(e)}")
            raise BaseAppException(f"Error creating lesson: {str(e)}") from e

    async def update_lesson(self, lesson_id: int, update_data: LessonSchemas.LessonUpdateRequest) -> Lesson:
        try:
            lesson = await self.get_lesson(lesson_id)

            if update_data.title:
                lesson.title = update_data.title
            if update_data.content:
                lesson.content = update_data.content
            if update_data.video_url:
                lesson.video_url = update_data.video_url
            if update_data.order_index is not None:
                lesson.order_index = update_data.order_index

            await self.db.commit()
            await self.db.refresh(lesson)
            return lesson
        except ResourceNotFoundException:
            raise
        except Exception as e:
            logger.exception(f"Error updating lesson: {str(e)}")
            raise BaseAppException(f"Error updating lesson: {str(e)}") from e

    async def delete_lesson(self, lesson_id: int) -> str:
        try:
            lesson = await self.get_lesson(lesson_id)
            await self.db.delete(lesson)
            await self.db.commit()
            return f"Lesson with id={lesson_id} deleted successfully"
        except ResourceNotFoundException:
            raise
        except Exception as e:
            logger.exception(f"Error deleting lesson: {str(e)}")
            raise BaseAppException(f"Error deleting lesson: {str(e)}") from e