from dataclasses import dataclass
from typing import Optional
from uuid import uuid4

from src.shared.exceptions import DomainError


@dataclass
class User:
    """
    User entity with core domain logic
    """

    first_name: str
    last_name: str
    username: str
    email: str
    identifier: str  # string of UUID
    _password: str
    id: Optional[int] = None

    def __str__(self) -> str:
        return f"{self.username}_{self.email}"

    def verify_password(self, password: str, hasher) -> bool:
        """
        Verifies the password of the user
        Args:
            User provided password
            Hasher service
        Returns :
            If password matches returns True else returns False
        """
        if hasher.verify(self._password, password):
            return True
        return False

    def change_password(self, password: str, hasher) -> None:
        """
        Changes the password of the user
        """
        if len(password) < 8:
            raise DomainError(detail="New password must be at least 8 characters")

        self._password = hasher.hash(password)

    def change_username(self, username: str) -> None:
        """
        Change the username of the user
        """
        self.username = username

    @classmethod
    def hash_password(cls, password: str, hasher) -> str:
        """
        Hashes the password using haser service
        Args:
            User provided password
            Hasher Service
        Returns
            Newly hashed password in string
        """
        return hasher.hash(password)

    @classmethod
    def create_user(
        cls,
        first_name: str,
        last_name: str,
        username: str,
        email: str,
        password: str,
        hasher,
        identifier: str = str(uuid4()),
    ) -> "User":
        """
        Creates the user
        Args
            first_name, last_name,username,email,identifier,password
        Returns
            instance of User class
        """
        if not username or not email:
            raise DomainError("Username and email is required.")

        return cls(
            id=None,  # will be overriden by the repository
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            _password=cls.hash_password(password, hasher),
            identifier=identifier,
        )
