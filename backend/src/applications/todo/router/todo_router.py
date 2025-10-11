from fastapi import APIRouter, Depends, Query
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from src.applications.todo.schemas.todo_schemas import (
    CreateTodoItemSchema,
    TodoItemOutSchema,
)
from src.shared.response import CustomResponse as cr
from src.shared.response import CustomResponseSchema

from ..schemas import CreateTodoListSchema, TodoListOutSchema
from ..services.todo_services import get_todo_services

router = APIRouter()


@router.post("/list", response_model=CustomResponseSchema[TodoListOutSchema])
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


@router.get("/list", response_model=CustomResponseSchema[list[TodoListOutSchema]])
async def list_all_todo_lists(todo_service=Depends(get_todo_services)):
    """
    lists all the todo lists
    """
    all_todo_list = await todo_service.list_todos()
    data = [
        TodoListOutSchema.model_validate(todo_list).model_dump()
        for todo_list in all_todo_list
    ]
    return cr.success(
        message="Successfully fetched the todo list",
        data=data,
        status_code=HTTP_200_OK,
    )


@router.delete("/list")
async def delete_todo_list(
    identifier: str = Query(..., title="Identifier"),
    todo_service=Depends(get_todo_services),
):
    """
    Delete todo list by identifier
    """
    await todo_service.delete_todo_list(identifier=identifier)
    return cr.success(status_code=HTTP_204_NO_CONTENT)


@router.post("/item", response_model=CustomResponseSchema[TodoItemOutSchema])
async def create_todo_item(
    payload: CreateTodoItemSchema, todo_service=Depends(get_todo_services)
):
    """
    Creates todo item
    """
    new_todo_item = await todo_service.create_todo_item(payload)
    return cr.success(
        message="Successfully created the todo item",
        data=TodoItemOutSchema.model_validate(new_todo_item).model_dump(),
        status_code=HTTP_201_CREATED,
    )


@router.get("/item", response_model=CustomResponseSchema[list[TodoItemOutSchema]])
async def list_all_todo_items(todo_service=Depends(get_todo_services)):
    """
    lists all the todo lists
    """
    all_todo_items = await todo_service.list_todo_items()
    data = [
        TodoItemOutSchema.model_validate(todo_list).model_dump()
        for todo_list in all_todo_items
    ]
    return cr.success(
        message="Successfully fetched the todo items",
        data=data,
        status_code=HTTP_200_OK,
    )


@router.delete("/item")
async def delete_todo_item(
    identifier: str = Query(..., title="Identifier"),
    todo_service=Depends(get_todo_services),
):
    """
    Delete todo item by identifier
    """
    await todo_service.delete_todo_item(identifier=identifier)
    return cr.success(status_code=HTTP_204_NO_CONTENT)
