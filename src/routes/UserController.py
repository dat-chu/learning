from fastapi import APIRouter, Depends
from src.dependencies import get_user_service
from src.service.UserService import UserService

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.get("", status_code=200)
async def get_user(username: str, service: UserService = Depends(get_user_service)):
    return await service.get_user(username)