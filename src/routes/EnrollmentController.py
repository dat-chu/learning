from fastapi import APIRouter, Depends, Request
from src.dependencies import get_enrollment_service
from src.schemas import EnrollmentSchemas
from src.service.EnrollmentService import EnrollmentService
from src.routes.utils import role_required

router = APIRouter(
    prefix="/enrollments",
    tags=["enrollments"],
)

@router.post("", status_code=201)
async def enroll_user(
    request: Request,
    enrollment: EnrollmentSchemas.EnrollmentCreateRequest,
    service: EnrollmentService = Depends(get_enrollment_service)
):
    return await service.enroll_user(enrollment)

@router.get("/user/{user_id}", status_code=200)
async def get_enrollments_by_user(
    user_id: int,
    service: EnrollmentService = Depends(get_enrollment_service)
):
    return await service.get_enrollments_by_user(user_id)

@router.get("/course/{course_id}", status_code=200)
async def get_enrollments_by_course(
    course_id: int,
    service: EnrollmentService = Depends(get_enrollment_service)
):
    return await service.get_enrollments_by_course(course_id)

@router.delete("/{enrollment_id}", status_code=204)
@role_required("admin")
async def remove_enrollment(
    enrollment_id: int,
    service: EnrollmentService = Depends(get_enrollment_service)
):
    await service.remove_enrollment(enrollment_id)
    return {"message": "Enrollment removed"}
