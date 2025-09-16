from fastapi import APIRouter, Depends, status
from src.dependencies import get_auth_service
from src.service.AuthService import AuthService
from src.schemas import AuthSchemas

router = APIRouter(
    prefix="/authentication",
    tags=["authentication"],
)

@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(user: AuthSchemas.UserSignupRequest, service: AuthService = Depends(get_auth_service)):
    return await service.signup(user)