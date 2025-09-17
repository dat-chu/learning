import logging
from src.repository.interfaces.interface_LessonRepository import LessonRepository as LessonRepositoryInterface
from src.schemas import LessonSchemas

logger = logging.getLogger(__name__)

class LessonService:
    def __init__(self, lesson_repository: LessonRepositoryInterface):
        self.lesson_repository = lesson_repository

    async def get_lesson(self, lesson_id: int) -> LessonSchemas.LessonResponse:
        lesson = await self.lesson_repository.get_lesson(lesson_id)
        return LessonSchemas.LessonResponse.model_validate(lesson)

    async def create_lesson(self, lesson_instance: LessonSchemas.LessonCreateRequest) -> LessonSchemas.LessonResponse:
        new_lesson = await self.lesson_repository.create_lesson(lesson_instance)
        return LessonSchemas.LessonResponse.model_validate(new_lesson)

    async def update_lesson(self, lesson_id: int, update_data: LessonSchemas.LessonUpdateRequest) -> LessonSchemas.LessonResponse:
        updated_lesson = await self.lesson_repository.update_lesson(lesson_id, update_data)
        return LessonSchemas.LessonResponse.model_validate(updated_lesson)

    async def delete_lesson(self, lesson_id: int) -> str:
        return await self.lesson_repository.delete_lesson(lesson_id)
    
    async def list_lessons_by_course(self, course_id: int) -> list[LessonSchemas.LessonResponse]:
        lessons = await self.lesson_repository.get_lessons_by_course(course_id)
        return [LessonSchemas.LessonResponse.model_validate(lesson) for lesson in lessons]
