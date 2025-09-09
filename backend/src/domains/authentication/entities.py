from dataclasses import dataclass
from uuid import UUID


@dataclass
class UserData:
    """
    User Data data class to hold data values
    """

    first_name: str
    last_name: str
    username: str
    email: str
    identifier: UUID
    password: str


class User:
    """
    User entities with attributes of user
    """

    def __init__(self, user_data: UserData) -> None:
        """
        Initializes the attributes
        """
        self.first_name = user_data.first_name
        self.last_name = user_data.last_name
        self.email = user_data.email
        self.identifier = user_data.identifier
        self.password = user_data.password
        self.username = user_data.username

    def __str__(self) -> str:
        return f"{self.username}_{self.email}"

    def change_password(self, password: str) -> None:
        """
        Changes the password of the user
        """
        self.password = password
