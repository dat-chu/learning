from fastapi import APIRouter, Depends, Request
from src.dependencies import get_course_service
from src.schemas import CourseSchemas
from src.service.CourseService import CourseService
from src.routes.utils import role_required

router = APIRouter(
    prefix="/courses",
    tags=["courses"],
)

@router.get("/{course_id}", status_code=200)
async def get_course(
    request: Request,
    course_id: int,
    service: CourseService = Depends(get_course_service),
):
    return await service.get_course(course_id)

@router.post("", status_code=201)
@role_required("admin")
async def create_course(
    request: Request,
    course_instance: CourseSchemas.CourseCreateRequest,
    service: CourseService = Depends(get_course_service),
):
    return await service.create_course(course_instance)

@router.put("/{course_id}", status_code=200)
@role_required("admin")
async def update_course(
    request: Request,
    course_id: int,
    course_instance: CourseSchemas.CourseUpdateRequest,
    service: CourseService = Depends(get_course_service),
):
    return await service.update_course(course_id, course_instance)

@router.delete("/{course_id}", status_code=200)
@role_required("admin")
async def delete_course(
    request: Request,
    course_id: int,
    service: CourseService = Depends(get_course_service),
):
    return await service.delete_course(course_id)

@router.get("", status_code=200)
async def list_courses(
    request: Request,
    service: CourseService = Depends(get_course_service),
):
    return await service.list_courses()