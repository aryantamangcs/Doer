from abc import ABC, abstractmethod
from typing import Any

from ..entities import User


class UserRepo(ABC):
    """
    Interface for User Repostiory
    """

    @abstractmethod
    async def add(self, user: User) -> User:
        """
        adds user
        Returns:
            User
        """

    @abstractmethod
    async def find_one(self, where, **kwargs) -> User | None:
        """
        Finds user
        Returns:
            User if found else None
        """

    @abstractmethod
    async def filter(self, where: dict[str, Any] | None = None, **kwargs) -> list[User]:
        """
        Finds  list of users
        Returns:
            List of users
        """

    @abstractmethod
    async def get_by_id(self, id: int) -> User | None:
        """
        Finds user
        Returns:
            User if found else None
        """

    @abstractmethod
    async def get_by_identifier(self, identifier: str) -> User | None:
        """
        Finds user
        Returns:
            User if found else None
        """

    @abstractmethod
    async def get_all(self, **kwargs) -> list[User]:
        """
        Finds  list of users
        Returns:
            List of users
        """

    @abstractmethod
    async def update(self, user: User, **kwargs) -> User:
        """
        Finds user
        Returns:
            Update users
        """

    @abstractmethod
    async def delete(self, **kwargs) -> None:
        """
        Deletes the user
        """

    @abstractmethod
    async def get_by_email(self, email: str) -> User | None:
        """
        Gets user by email if exists
        Returns :
            User if found by email else returns None
        """

    @abstractmethod
    async def get_by_username(self, username: str) -> User | None:
        """
        Gets user by username if exists
        Returns :
            User if found by username else returns None
        """
