from fastapi import APIRouter, Depends
from src.dependencies import get_user_service
from src.schemas import UserSchemas
from src.service.UserService import UserService
from src.routes.utils import role_required
from fastapi import Request

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.get("", status_code=200)
@role_required("admin")
async def get_user(request: Request, username: str, service: UserService = Depends(get_user_service)):
    return await service.get_user(username)

@router.post("", status_code=201)
@role_required("admin")
async def create_user(request: Request, user_instance: UserSchemas.UserCreateRequest, service: UserService = Depends(get_user_service)):
    return await service.create_user(user_instance)