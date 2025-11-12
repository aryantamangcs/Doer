from abc import ABC, abstractmethod
from typing import Any

from ...shared.base_domain_repository import BaseDomainRepository
from ..entities import User


class UserRepo(BaseDomainRepository[User]):
    """
    Interface for User Repostiory
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
