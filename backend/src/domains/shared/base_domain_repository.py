from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

T = TypeVar("T")


class BaseDomainRepository(ABC, Generic[T]):
    """
    base repository for domains
    """

    @abstractmethod
    async def add(self, entity: T) -> T:
        """
        adds entity
        Returns:
            T
        """

    @abstractmethod
    async def find_one(self, where: dict[str, Any], **kwargs) -> T | None:
        """
        finds entity on the basis of where conditions
        Returns:
            if found T else None
        """

    @abstractmethod
    async def filter(self, where: dict[str, Any] | None = None, **kwargs) -> list[T]:
        """
        Finds  list of entity
        Returns:
            List of entitiy
        """

    @abstractmethod
    async def get_by_id(self, id: int) -> T | None:
        """
        Finds entity by id
        Returns:
            T if found else None
        """

    @abstractmethod
    async def get_by_identifier(self, identifier: str) -> T | None:
        """
        Finds entity
        Returns:
            T if found else None
        """

    @abstractmethod
    async def get_all(self, **kwargs) -> list[T]:
        """
        Finds  list of entity
        Returns:
            List of T
        """

    @abstractmethod
    async def update(self, entity: T, **kwargs) -> T:
        """
        Updates the entity
        Returns:
            Updated T
        """

    @abstractmethod
    async def delete(self, **kwargs) -> None:
        """
        Deletes the entity
        """
