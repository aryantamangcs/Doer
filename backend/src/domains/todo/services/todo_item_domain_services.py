from src.domains.todo.entities.todo_item_entity import TodoItem
from src.domains.todo.enums.todo_enums import TodoStatusEnum
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
            raise NotFoundError("Todo list  not found")

        if not todo_list.id:
            raise ServerError("Todo list id is set none")

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

    async def delete_todo_item(self, todo_id) -> None:
        """
        Delete the todo item
        """

        todo_item = await self.repo.get_by_id(id=todo_id)
        if not todo_item:
            raise ValueError("Todo item not found while deleting")
        return await self.repo.delete(id=todo_id)
