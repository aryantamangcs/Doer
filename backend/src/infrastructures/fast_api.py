from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.applications.authentication.router import auth_router

from .exception_handler import add_exceptions_handler


def create_app():
    """
    Creates and configures the fastapi application
    """
    app = FastAPI(
        title="Doer Application", description="A simple project for leveling up"
    )

    main_router = APIRouter(prefix="/api")
    main_router.include_router(auth_router)

    app.include_router(main_router)

    # global exception handlers
    add_exceptions_handler(app)

    # middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # allowed origins
        allow_credentials=True,  # allow cookies/auth headers
        allow_methods=["*"],  # allow all HTTP methods (GET, POST, etc.)
        allow_headers=["*"],  # allow all headers
    )

    return app
