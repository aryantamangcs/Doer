from typing import Protocol


class PasswordHasher(Protocol):
    """
    Password hasher interface
    """

    def hash(self, value: str) -> str: ...

    def verify(self, hashed_value: str, value: str) -> bool: ...
