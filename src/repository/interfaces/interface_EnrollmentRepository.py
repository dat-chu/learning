from abc import ABC, abstractmethod
from typing import List, Optional
from src.schemas import EnrollmentSchemas
from src.repository.implementations.PostgreSQL.models.index import Enrollment

class EnrollmentRepository(ABC):

    @abstractmethod
    async def enroll_user(self, enrollment: EnrollmentSchemas.EnrollmentCreateRequest) -> Enrollment:
        pass

    @abstractmethod
    async def get_enrollments_by_user(self, user_id: int) -> List[Enrollment]:
        pass

    @abstractmethod
    async def get_enrollments_by_course(self, course_id: int) -> List[Enrollment]:
        pass

    @abstractmethod
    async def remove_enrollment(self, enrollment_id: int) -> str:
        pass
