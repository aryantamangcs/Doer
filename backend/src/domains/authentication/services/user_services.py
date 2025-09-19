from ..repositories import UserRepo
from .password_hasher import PasswordHasher


class UserServices:
    """
    List of methods and attributes for UserServices
    """

    def __init__(self, user_repo: UserRepo):
        self.user_repo = user_repo

    async def check_email_already_exists(self, email: str) -> bool:
        """
        Checks email already exists or not
        Returns:
            True if email already exists
            Else False
        """
        email_exists = await self.user_repo.get_by_email(email)
        if not email_exists:
            return False
        return True

    async def check_username_already_exists(self, username: str) -> bool:
        """
        Checks username already exists or not
        Returns:
            True if username already exists
            Else False
        """
        username_exists = await self.user_repo.get_by_username(username)
        if not username_exists:
            return False
        return True

    def hash_password(self, password: str, hasher: PasswordHasher) -> str:
        """
        Hashes the password and returns the hashed password
        """
        return hasher.hash(password)

    def verify_password(
        self, hashed_password: str, password: str, hasher: PasswordHasher
    ) -> bool:
        """
        Verifies the password
        Args:
            hashed_password
            password
        Returns:
            True if password is verified else False
        """

        return hasher.verify(hashed_password, password)
