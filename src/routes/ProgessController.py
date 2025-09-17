from fastapi import APIRouter, Depends, Request
from src.dependencies import get_progress_service
from src.schemas import ProgressSchemas
from src.service.ProgressService import ProgressService

router = APIRouter(
    prefix="/progress",
    tags=["progress"],
)

@router.post("", status_code=201)
async def mark_progress(request: Request, progress: ProgressSchemas.ProgressCreateRequest, service: ProgressService = Depends(get_progress_service)):
    return await service.mark_progress(progress)

@router.put("/{progress_id}", status_code=200)
async def update_progress(request: Request, progress_id: int, update: ProgressSchemas.ProgressUpdateRequest, service: ProgressService = Depends(get_progress_service)):
    return await service.update_progress(progress_id, update)

@router.get("/course/{course_id}/user/{user_id}", status_code=200)
async def get_progress_percentage(request: Request, user_id: int, course_id: int, service: ProgressService = Depends(get_progress_service)):
    return {"progress_percentage": await service.get_user_progress_in_course(user_id, course_id)}
