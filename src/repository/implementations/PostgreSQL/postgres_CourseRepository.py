import logging
from sqlalchemy import select
from src.exceptions import BaseAppException, ResourceNotFoundException
from src.schemas import CourseSchemas
from src.repository.implementations.PostgreSQL.models.index import Course
from src.repository.implementations.PostgreSQL.utils import get_course_by_id
from src.repository.interfaces.interface_CourseRepository import CourseRepository as CourseRepositoryInterface

logger = logging.getLogger(__name__)

class CourseRepository(CourseRepositoryInterface):
    def __init__(self, db=None):
        self.db = db

    async def get_course(self, course_id: int) -> Course:
        try:
            course = await get_course_by_id(self.db, course_id)
            if not course:
                raise ResourceNotFoundException(f"Course with id={course_id} not found")
            return course

        except ResourceNotFoundException:
            raise
        except Exception as e:
            logger.exception(f"Error getting course: {str(e)}")
            raise BaseAppException(f"Internal database error: {str(e)}") from e

    async def create_course(self, course_instance: CourseSchemas.CourseCreateRequest) -> Course:
        try:
            new_course = Course(
                title=course_instance.title,
                description=course_instance.description,
            )
            self.db.add(new_course)
            await self.db.commit()
            await self.db.refresh(new_course)
            return new_course
        except Exception as e:
            logger.exception(f"Error creating course: {str(e)}")
            raise BaseAppException(f"Error creating course: {str(e)}") from e

    async def update_course(self, course_id: int, update_data: CourseSchemas.CourseUpdateRequest) -> Course:
        try:
            course = await self.get_course(course_id)

            if update_data.title:
                course.title = update_data.title
            if update_data.description:
                course.description = update_data.description

            await self.db.commit()
            await self.db.refresh(course)
            return course

        except ResourceNotFoundException:
            raise
        except Exception as e:
            logger.exception(f"Error updating course: {str(e)}")
            raise BaseAppException(f"Error updating course: {str(e)}") from e

    async def delete_course(self, course_id: int) -> str:
        try:
            course = await self.get_course(course_id)
            await self.db.delete(course)
            await self.db.commit()
            return f"Course with id={course_id} deleted successfully"

        except ResourceNotFoundException:
            raise
        except Exception as e:
            logger.exception(f"Error deleting course: {str(e)}")
            raise BaseAppException(f"Error deleting course: {str(e)}") from e
        
    async def list_courses(self) -> list[Course]:
        try:
            result = await self.db.execute(select(Course))
            courses = result.scalars().all()
            return courses
        except Exception as e:
            logger.exception(f"Error listing courses: {str(e)}")
            raise BaseAppException(f"Internal database error: {str(e)}") from e
        
    
