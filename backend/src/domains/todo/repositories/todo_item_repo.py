from abc import ABC, abstractmethod
from typing import Callable

from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructures.db.config import async_session

from ..entities.todo_item_entity import TodoItem


class TodoItemRepository(ABC):
    """
    List of interfaces for todo item repository
    """

    @abstractmethod
    async def add(self, todo_item: TodoItem) -> TodoItem:
        """
        Adds the todoitem and returns an instance of todo item
        """
        raise NotImplementedError

    @abstractmethod
    async def find_one(self, where: dict | None = None, **kwargs):
        """
        Finds one todo item
        """
        raise NotImplementedError

    @abstractmethod
    async def filter(self, where: dict | None = None, **kwargs) -> list[TodoItem]:
        """
        Finds item of todo on certain conditions
        """

    @abstractmethod
    async def get_all(self) -> list[TodoItem]:
        """
        Finds todo item
        """
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: int) -> None:
        """
        Delets the todo item
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, id: int) -> TodoItem | None:
        """
        Get Todo Item by id
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_identifier(self, identifier: str) -> TodoItem | None:
        """
        Get Todo Item by identifier
        """
        raise NotImplementedError
