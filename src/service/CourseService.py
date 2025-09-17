import logging
from src.repository.interfaces.interface_CourseRepository import CourseRepository as CourseRepositoryInterface
from src.schemas import CourseSchemas

logger = logging.getLogger(__name__)


class CourseService:
    def __init__(self, course_repository: CourseRepositoryInterface):
        self.course_repository = course_repository

    async def get_course(self, course_id: int) -> CourseSchemas.CourseResponse:
        course = await self.course_repository.get_course(course_id)
        return CourseSchemas.CourseResponse.model_validate(course)

    async def create_course(
        self,
        course_instance: CourseSchemas.CourseCreateRequest
    ) -> CourseSchemas.CourseResponse:
        new_course = await self.course_repository.create_course(course_instance)
        return CourseSchemas.CourseResponse.model_validate(new_course)

    async def update_course(
        self,
        course_id: int,
        update_data: CourseSchemas.CourseUpdateRequest
    ) -> CourseSchemas.CourseResponse:
        updated_course = await self.course_repository.update_course(course_id, update_data)
        return CourseSchemas.CourseResponse.model_validate(updated_course)

    async def delete_course(self, course_id: int) -> str:
        return await self.course_repository.delete_course(course_id)
