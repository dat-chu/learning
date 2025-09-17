from fastapi import APIRouter, Depends, Request
from src.dependencies import get_lesson_service
from src.schemas import LessonSchemas
from src.service.LessonService import LessonService
from src.routes.utils import role_required

router = APIRouter(
    prefix="/lessons",
    tags=["lessons"],
)

@router.get("/{lesson_id}", status_code=200)
async def get_lesson(
    request: Request,
    lesson_id: int,
    service: LessonService = Depends(get_lesson_service),
):
    return await service.get_lesson(lesson_id)

@router.post("", status_code=201)
@role_required("admin")
async def create_lesson(
    request: Request,
    lesson_instance: LessonSchemas.LessonCreateRequest,
    service: LessonService = Depends(get_lesson_service),
):
    return await service.create_lesson(lesson_instance)

@router.put("/{lesson_id}", status_code=200)
@role_required("admin")
async def update_lesson(
    request: Request,
    lesson_id: int,
    lesson_instance: LessonSchemas.LessonUpdateRequest,
    service: LessonService = Depends(get_lesson_service),
):
    return await service.update_lesson(lesson_id, lesson_instance)

@router.delete("/{lesson_id}", status_code=200)
@role_required("admin")
async def delete_lesson(
    request: Request,
    lesson_id: int,
    service: LessonService = Depends(get_lesson_service),
):
    return await service.delete_lesson(lesson_id)

@router.get("/by_course/{course_id}", status_code=200)
async def list_lessons_by_course(
    request: Request,
    course_id: int,
    service: LessonService = Depends(get_lesson_service),
):
    return await service.list_lessons_by_course(course_id)
