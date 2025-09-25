from src.domains.todo.entities.todo_item_entity import TodoItem
from src.domains.todo.enums.todo_enums import TodoStatusEnum

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
        todo_list_id: int,
        title: str,
        status: TodoStatusEnum,
        description: str,
        owner_id: int,
    ) -> TodoItem:
        """
        Creates todo item and returns the new todo item
        """
        todo_list = self.todo_list_repo.get_by_id(id=todo_list_id)

        if not todo_list:
            raise ValueError("Todo list id not found")

        new_item = TodoItem.create(
            todo_list_id=todo_list_id,
            title=title,
            status=status,
            description=description,
            owner_id=owner_id,
        )
        return await self.repo.add(new_item)

    async def delete(self, todo_id) -> None:
        """
        Delete the todo item
        """

        todo_item = await self.repo.get_by_id(id=todo_id)
        if not todo_item:
            raise ValueError("Todo item not found while deleting")
        return await self.repo.delete(id=todo_id)
