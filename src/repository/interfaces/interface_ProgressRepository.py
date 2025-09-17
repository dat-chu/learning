from abc import ABC, abstractmethod
from src.schemas import ProgressSchemas
from src.repository.implementations.PostgreSQL.models.index import Progress

class ProgressRepository(ABC):

    @abstractmethod
    async def mark_progress(self, progress: ProgressSchemas.ProgressCreateRequest) -> Progress:
        pass

    @abstractmethod
    async def update_progress(self, progress_id: int, update: ProgressSchemas.ProgressUpdateRequest) -> Progress:
        pass

    @abstractmethod
    async def get_user_progress_in_course(self, user_id: int, course_id: int) -> float:
        """Return percentage of completed lessons in a course"""
        pass
