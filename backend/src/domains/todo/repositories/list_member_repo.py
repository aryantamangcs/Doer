from abc import ABC, abstractmethod
from typing import Any, Optional

from src.domains.todo.entities.todo_entity import ListMember

from ..enums.todo_enums import TodoListMemberRoleEnum


class ListMemberRepo(ABC):
    """
    list of interfaces for list member
    """

    @abstractmethod
    async def add(self, member: ListMember) -> ListMember:
        """
        Adds member to the list member
        """
        raise NotImplementedError

    @abstractmethod
    async def find_one(self, where: dict[str, Any] | None, **kwargs) -> ListMember:
        """
        Returns the list member instance
        """
        raise NotImplementedError

    @abstractmethod
    async def delete(self, member: ListMember):
        """
        removes member from the list member
        """
        raise NotImplementedError
