from src.repository.interfaces.interface_ProgressRepository import ProgressRepository
from src.schemas import ProgressSchemas

class ProgressService:
    def __init__(self, progress_repository: ProgressRepository):
        self.progress_repository = progress_repository

    async def mark_progress(self, progress: ProgressSchemas.ProgressCreateRequest) -> ProgressSchemas.ProgressResponse:
        new_progress = await self.progress_repository.mark_progress(progress)
        return ProgressSchemas.ProgressResponse.model_validate(new_progress)

    async def update_progress(self, progress_id: int, update: ProgressSchemas.ProgressUpdateRequest) -> ProgressSchemas.ProgressResponse:
        updated = await self.progress_repository.update_progress(progress_id, update)
        return ProgressSchemas.ProgressResponse.model_validate(updated)

    async def get_user_progress_in_course(self, user_id: int, course_id: int) -> float:
        return await self.progress_repository.get_user_progress_in_course(user_id, course_id)
