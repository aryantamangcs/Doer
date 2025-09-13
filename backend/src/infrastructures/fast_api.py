from fastapi import APIRouter, FastAPI

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

    return app
