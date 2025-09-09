from abc import ABC, abstractmethod

from ..entities import User


class UserRepo(ABC):
    """
    Interface for User Repostiory
    """

    @abstractmethod
    async def create(self, user: User) -> User:
        """
        Creates user
        Returns:
            User
        """

    @abstractmethod
    async def find_one(self, **kwargs) -> User | None:
        """
        Finds user
        Returns:
            User if found else None
        """

    @abstractmethod
    async def filter(self, **kwargs) -> list[User]:
        """
        Finds  list of users
        Returns:
            List of users
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
