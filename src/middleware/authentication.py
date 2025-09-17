import jwt
from src.db.settings import get_settings
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        if request.url.path in ["/authentication/login", "/authentication/signup", "/docs", "/openapi.json"]:
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            from starlette.responses import JSONResponse
            return JSONResponse({"detail": "Unauthorized"}, status_code=401)
        token = auth_header.split(" ")[1]
        settings = get_settings()
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            request.state.user_id = payload.get("sub")
            request.state.username = payload.get("username")
            request.state.role = payload.get("role")
            if request.state.user_id is None:
                from starlette.responses import JSONResponse
                return JSONResponse({"detail": "Unauthorized"}, status_code=401)
        except jwt.ExpiredSignatureError:
            from starlette.responses import JSONResponse
            return JSONResponse({"detail": "Token has expired"}, status_code=401)
        except jwt.InvalidTokenError:
            from starlette.responses import JSONResponse
            return JSONResponse({"detail": "Invalid token"}, status_code=401)

        response = await call_next(request)
        return response