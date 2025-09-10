import uvicorn
from fastapi import APIRouter, FastAPI

from src.applications.authentication.router import auth_router

app = FastAPI(title="Doer Application", description="A simple project for leveling up")

main_router = APIRouter(prefix="/api")
main_router.include_router(auth_router)

app.include_router(main_router)
