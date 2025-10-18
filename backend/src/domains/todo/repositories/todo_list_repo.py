from abc import ABC, abstractmethod
from typing import Any

from ..entities.todo_entity import TodoList


class TodoListRepository(ABC):
    """
    List of interfaces for todo list repository
    """

    @abstractmethod
    async def add(self, todo_list: TodoList) -> TodoList:
        """
        Adds the todolist and returns an instance of todo list
        """
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> list[TodoList]:
        """
        Adds the todolist and returns an instance of todo list
        """
        raise NotImplementedError

    @abstractmethod
    async def find_one(self, where: dict | None = None, **kwargs) -> TodoList | None:
        """
        Finds one todo list
        """
        raise NotImplementedError

    @abstractmethod
    async def filter(
        self, where: dict | None = None, related: list[Any] | None = None, **kwargs
    ) -> list[TodoList]:
        """
        Finds list of todo on certain conditions
        """

    @abstractmethod
    async def delete(self, id: int):
        """
        Delets the todo list
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, id: int) -> TodoList | None:
        """
        Returns the TodoList instance by id if found else returns none
        """
        raise NotImplementedError

    @abstractmethod
    async def update(self, updated_todo_list: TodoList) -> TodoList | None:
        """
        Updates the todo_list and returns updated list
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_identifier(self, identifier: str) -> TodoList | None:
        """
        Get Todo Item by identifier
        """
        raise NotImplementedError
