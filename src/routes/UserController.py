from fastapi import APIRouter, Depends
from src.dependencies import get_service
from src.service.Service import Service

router = APIRouter(
    prefix="/users"
)

@router.get("", status_code=200)
async def get_user(
    email: str,
    service: Service = Depends(get_service)):
    return await service.get_user(email=email)