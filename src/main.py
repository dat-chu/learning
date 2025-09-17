from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import UserController, AuthController
from .exceptions import BaseAppException
import logging
from src.logging_config import setup_logging
from fastapi.responses import JSONResponse
from src.middleware.correlation_id_middleware import CorrelationIdMiddleware
from src.middleware.authentication import AuthMiddleware
from contextlib import asynccontextmanager
from src.db.settings import get_settings, DatabaseType
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

setup_logging()
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code (runs before application startup)
    # This is where you put code that was previously in @app.on_event("startup")
    logger.info("Running startup tasks...")

    # Initialize settings
    settings = get_settings()
    if settings.DATABASE_TYPE == DatabaseType.POSTGRES:
        # Create an async engine
        engine = create_async_engine(settings.POSTGRES_DATABASE_URL, echo=True, future=True)

        # Create an async sessionmaker factory
        app.state.postgres_session = async_sessionmaker(
            bind=engine,
            expire_on_commit=False,  # optional: objects stay active after commit
            class_=AsyncSession
        )

    logger.info("Startup tasks completed")
    yield
    # Shutdown code (runs after application shutdown)
    logger.info("Running shutdown tasks...")
    logger.info("Shutdown tasks completed")
    # This is where you put code that was previously in @app.on_event("shutdown")

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "PUT"],
    allow_headers=["Authorization", "Content-Type"]
)

# Enable Correlation ID middleware
app.add_middleware(CorrelationIdMiddleware)
app.add_middleware(AuthMiddleware)

# Global exception handler
@app.exception_handler(BaseAppException)
async def app_exception_handler(request, exc):
    logger.error("Application error: %s", exc.message)
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.message}
    )


app.include_router(UserController.router)
app.include_router(AuthController.router)