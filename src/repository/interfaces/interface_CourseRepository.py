from abc import ABC, abstractmethod
from src.schemas import CourseSchemas
from src.repository.implementations.PostgreSQL.models.index import Course

class CourseRepository(ABC):

    @abstractmethod
    async def get_course(self, course_id: int) -> Course:
        """Get course by id"""
        pass

    @abstractmethod
    async def create_course(self, course_instance: CourseSchemas.CourseCreateRequest) -> Course:
        """Create a new course"""
        pass

    @abstractmethod
    async def update_course(self, course_id: int, update_data: CourseSchemas.CourseUpdateRequest) -> Course:
        """Update an existing course"""
        pass

    @abstractmethod
    async def delete_course(self, course_id: int) -> str:
        """Delete a course by id"""
        pass