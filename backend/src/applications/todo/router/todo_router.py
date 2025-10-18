from fastapi import APIRouter, Depends, Query
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from src.applications.todo.schemas.todo_schemas import (
    CreateTodoItemSchema,
    CreateTodoListMemberSchema,
    EditTodoItemSchema,
    EditTodoListSchema,
    TodoItemOutSchema,
    TodoListMemberSchema,
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


@router.patch("/list", response_model=CustomResponseSchema[list[TodoItemOutSchema]])
async def edit_todo_list(
    payload: EditTodoListSchema,
    todo_list_identifier: str = Query(
        ..., title="Todo list identifier of which you want to edit details"
    ),
    todo_service=Depends(get_todo_services),
):
    """
    Edit todo item details
    """
    updated_list = await todo_service.edit_todo_list(todo_list_identifier, payload)
    return cr.success(
        message="Successfully updated the todo list",
        data=TodoListOutSchema.model_validate(updated_list).model_dump(),
        status_code=HTTP_200_OK,
    )


@router.post("/list/add-member", response_model=CustomResponseSchema)
async def todo_list_add_member(
    payload: CreateTodoListMemberSchema, todo_service=Depends(get_todo_services)
):
    """
    Add member to the todo_list
    """
    await todo_service.todo_list_add_member(payload)
    return cr.success(message="Successfully added member", status_code=HTTP_201_CREATED)


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
async def list_all_todo_items(
    todo_list_identifier: str = Query(
        ..., title="Todo list identifier of which you want to list todo_item"
    ),
    todo_service=Depends(get_todo_services),
):
    """
    lists all the todo lists
    """
    all_todo_items = await todo_service.list_todo_items(todo_list_identifier)
    data = [
        TodoItemOutSchema.model_validate(todo_list).model_dump()
        for todo_list in all_todo_items
    ]
    return cr.success(
        message="Successfully fetched the todo items",
        data=data,
        status_code=HTTP_200_OK,
    )


@router.patch("/item", response_model=CustomResponseSchema[list[TodoItemOutSchema]])
async def edit_todo_item(
    payload: EditTodoItemSchema,
    todo_item_identifier: str = Query(
        ..., title="Todo item identifier of which you want to edit details"
    ),
    todo_service=Depends(get_todo_services),
):
    """
    Edit todo item details
    """
    updated_item = await todo_service.edit_todo_item(todo_item_identifier, payload)
    return cr.success(
        message="Successfully updated the todo item",
        data=TodoItemOutSchema.model_validate(updated_item).model_dump(),
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
