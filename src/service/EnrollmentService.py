from src.repository.interfaces.interface_EnrollmentRepository import EnrollmentRepository as EnrollmentRepositoryInterface
from src.schemas import EnrollmentSchemas

class EnrollmentService:

    def __init__(self, enrollment_repository: EnrollmentRepositoryInterface):
        self.enrollment_repository = enrollment_repository

    async def enroll_user(self, enrollment: EnrollmentSchemas.EnrollmentCreateRequest):
        res = await self.enrollment_repository.enroll_user(enrollment)
        return EnrollmentSchemas.EnrollmentResponse.model_validate(res)

    async def get_enrollments_by_user(self, user_id: int):
        res = await self.enrollment_repository.get_enrollments_by_user(user_id)
        return [EnrollmentSchemas.EnrollmentResponse.model_validate(enrollment) for enrollment in res]

    async def get_enrollments_by_course(self, course_id: int):
        res = await self.enrollment_repository.get_enrollments_by_course(course_id)
        return [EnrollmentSchemas.EnrollmentResponse.model_validate(enrollment) for enrollment in res]

    async def remove_enrollment(self, enrollment_id: int):
        return await self.enrollment_repository.remove_enrollment(enrollment_id)
