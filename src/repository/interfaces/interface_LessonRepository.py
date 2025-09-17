from abc import ABC, abstractmethod
from typing import List, Optional
from src.schemas import LessonSchemas
from src.repository.implementations.PostgreSQL.models.index import Lesson


class LessonRepository(ABC):

    @abstractmethod
    async def get_lesson(self, lesson_id: int) -> Optional[Lesson]:
        pass

    @abstractmethod
    async def get_lessons_by_course(self, course_id: int) -> List[Lesson]:
        pass

    @abstractmethod
    async def create_lesson(self, lesson_instance: LessonSchemas.LessonCreateRequest) -> Lesson:
        pass

    @abstractmethod
    async def update_lesson(self, lesson_instance: LessonSchemas.LessonUpdateRequest) -> Lesson:
        pass

    @abstractmethod
    async def delete_lesson(self, lesson_id: int) -> str:
        pass