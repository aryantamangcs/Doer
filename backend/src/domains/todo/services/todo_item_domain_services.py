from datetime import date
from typing import Any

from src.domains.todo.entities.todo_item_entity import TodoItem
from src.domains.todo.enums.todo_enums import TodoStatusEnum
from src.infrastructures.authentication.repository.user_repo_sqlalchemy import (
    UserRepoSqlAlchemy,
)
from src.shared.exceptions import CreateError, NotFoundError, ServerError

from ..enums import TodoStatusEnum
from ..repositories.todo_item_repo import TodoItemRepository
from ..repositories.todo_list_repo import TodoListRepository


class TodoItemDomainServices:
    """
    list of methods and services for todo item
    """

    def __init__(self, repo: TodoItemRepository, todo_list_repo: TodoListRepository):
        self.repo = repo
        self.todo_list_repo = todo_list_repo

    async def create_todo_item(
        self,
        todo_list_identifier: str,
        title: str,
        status: TodoStatusEnum,
        description: str,
        owner_id: int,
    ) -> TodoItem:
        """
        Creates todo item and returns the new todo item
        """

        todo_list = await self.todo_list_repo.get_by_identifier(
            identifier=todo_list_identifier
        )
        if not todo_list:
            raise NotFoundError(detail="Todo list not found")

        if not todo_list.id:
            raise ServerError(detail="Todo list id is set none")

        new_item = TodoItem.create(
            todo_list_id=todo_list.id,
            title=title,
            status=status,
            description=description,
            owner_id=owner_id,
        )
        try:
            data = await self.repo.add(new_item)
            return data
        except Exception as e:
            raise CreateError(
                detail="Error while creating todo item", data=str(e)
            ) from e

    async def list_todo_item_by_todo_list(
        self, todo_list_identifier: str, req_date: date | None
    ) -> list[TodoItem]:
        """
        list all the todo item
        if the req_date is not provided the current date is used
        """
        todo_list = await self.todo_list_repo.get_by_identifier(todo_list_identifier)
        if not todo_list:
            raise NotFoundError(detail="Todo list not found")
        if not todo_list.id:
            raise ServerError(detail="Todo list id is set none")

        todo_items = await self.repo.filter_by_date(
            todo_list_id=todo_list.id, target_date=req_date or date.today()
        )
        return todo_items

    async def delete_todo_item(self, identifier: str) -> None:
        """
        Delete the todo item
        """

        todo_item = await self.repo.get_by_identifier(identifier=identifier)
        if not todo_item:
            raise ValueError("Todo item not found while deleting")
        if not todo_item.id:
            raise ValueError("Todo item id is set none")
        return await self.repo.delete(id=todo_item.id)

    async def edit_todo_item(
        self, todo_item_identifier: str, payload: dict[str, Any]
    ) -> TodoItem | None:
        """
        Edits the todo_item
        """
        todo_item = await self.repo.get_by_identifier(todo_item_identifier)
        if not todo_item:
            raise NotFoundError(detail="Todo item not found")
        for keys in payload.keys():
            match keys:
                case "title":
                    todo_item.change_title(title=payload["title"])
                case "status":
                    todo_item.change_status(status=payload["status"])
                case "description":
                    todo_item.change_description(description=payload["description"])
                case "owner_identifier":
                    user = await self.handle_owner_during_edit(
                        owner_identifier=payload["owner_identifier"]
                    )
                    if not user:
                        raise NotFoundError(detail="Owner identifier not found")
                    if not user.id:
                        raise ServerError(detail="User id is set none")
                    todo_item.change_owner(owner_id=user.id)
                case _:
                    return None

        updated_item = await self.repo.update(todo_item)
        return updated_item

    async def handle_owner_during_edit(self, owner_identifier: str):
        """
        Checks if the owner id exists or not
        """
        return await UserRepoSqlAlchemy().get_by_identifier(owner_identifier)
