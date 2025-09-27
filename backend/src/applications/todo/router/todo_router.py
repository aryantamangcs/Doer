from fastapi import APIRouter, Depends
from starlette.status import HTTP_201_CREATED

from src.shared.response import CustomResponse as cr
from src.shared.response import CustomResponseSchema

from ..schemas import CreateTodoListSchema, TodoListOutSchema
from ..services.todo_services import get_todo_services

router = APIRouter()


@router.post("/list", response_model=CustomResponseSchema)
async def create_todo_list(
    payload: CreateTodoListSchema, todo_service=Depends(get_todo_services)
):
    """
    Creates todo list
    """
    new_todo_list = await todo_service.create_todo_list(payload)
    return cr.success(
        message="Successfully created the todo list",
        data=TodoListOutSchema.model_validate(new_todo_list).model_dump(),
        status_code=HTTP_201_CREATED,
    )
