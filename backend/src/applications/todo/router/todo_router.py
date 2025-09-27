from fastapi import APIRouter

from src.shared.response import CustomResponseSchema

from ..schemas import CreateTodoListSchema

router = APIRouter(prefix="/todo")


@router.post("/list", response_model=CustomResponseSchema)
def create_todo_list(payload: CreateTodoListSchema):
    """
    Creates todo list
    """
