from abc import ABC, abstractmethod

from ..entities import User


class UserRepo(ABC):
    """
    Interface for User Repostiory
    """

    @abstractmethod
    def create(self, user: User) -> User:
        """
        Creates user
        Returns:
            User
        """

    @abstractmethod
    def find_one(self, **kwargs) -> User | None:
        """
        Finds user
        Returns:
            User if found else None
        """

    @abstractmethod
    def filter(self, **kwargs) -> list[User]:
        """
        Finds  list of users
        Returns:
            List of users
        """

    @abstractmethod
    def update(self, user: User, **kwargs) -> User:
        """
        Finds user
        Returns:
            Update users
        """

    @abstractmethod
    def delete(self, **kwargs) -> None:
        """
        Deletes the user
        """
