from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.applications.authentication.router import auth_router
from src.applications.journal.router import router as journal_router
from src.applications.todo.router import router as todo_router
from src.infrastructures.config.settings import get_settings
from src.infrastructures.middleware import AuthMiddleware

from .exception_handler import add_exceptions_handler

settings = get_settings()


def create_app():
    """
    Creates and configures the fastapi application
    """
    app = FastAPI(
        title="Doer Application", description="A simple project for leveling up"
    )

    main_router = APIRouter(prefix="/api")
    main_router.include_router(auth_router)
    main_router.include_router(todo_router)
    main_router.include_router(journal_router)

    app.include_router(main_router)

    # global exception handlers
    add_exceptions_handler(app)

    # middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOW_ORIGINS,
        allow_credentials=True,  # allow cookies/auth headers
        allow_methods=["*"],  # allow all HTTP methods (GET, POST, etc.)
        allow_headers=["*"],  # allow all headers
    )
    app.add_middleware(
        AuthMiddleware,
        exclude_path=[
            "/api/auth/login",
            "/api/auth/signup",
            "/api/auth/check-user",
            "/api/auth/refresh-token",
            "/docs",
            "/openapi.json",
        ],
    )

    return app
