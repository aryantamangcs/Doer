import uuid
from dataclasses import dataclass
from typing import Optional

from src.shared.exceptions import InvalidError


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

    def change_password(self, password: str) -> bool:
        """
        Changes the password of the user
        Args:
            password :- ! Hashed password should be provided
        Returns:
            True if password change is successful else False
        """
        try:
            self._password = password
            return True
        except Exception:  # pylint: disable=broad-except
            return False

    def change_username(self, username: str) -> bool:
        """
        Change the username of the user
        """
        try:
            self.username = username
            return True
        except Exception:  # pylint: disable=broad-except
            return False

    @classmethod
    def create_user(
        cls,
        first_name: str,
        last_name: str,
        username: str,
        email: str,
        password: str,
    ) -> "User":
        """
        Creates the user
        Args
            first_name, last_name,username,email,identifier,password
            password:- ! Password must be hashed
        Returns
            instance of User class
        """
        if not username or not email:
            raise InvalidError(detail="Username and email is required.")

        return cls(
            id=None,  # will be overriden by the repository
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            _password=password,
            identifier=str(uuid.uuid4()),
        )
