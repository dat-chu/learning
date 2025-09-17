from functools import wraps
from fastapi import HTTPException, Request
from src.exceptions import UnauthorizedException

def role_required(role: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request = kwargs.get("request")
            if not isinstance(request, Request):
                raise HTTPException(
                    status_code=400,
                    detail="Invalid or missing request object"
                )
            if request.state.role != role:
                raise UnauthorizedException(
                    f"User does not have the required role: {role}"
                )
            return await func(*args, **kwargs)
        return wrapper
    return decorator