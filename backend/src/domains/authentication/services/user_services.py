import bcrypt

from ..entities import User
from ..repositories import UserRepo


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

    def hash_password(self, password: str) -> str:
        """
        Hashes the password using bcrypt
        Returns:
            It returns the hashed password
        """
        byte_password = password.encode()
        hashed_password = bcrypt.hashpw(byte_password, bcrypt.gensalt())
        return hashed_password.decode()

    async def verify_password(self, hashed_password: str, password: str) -> bool:
        """
        Checks if the hashed_password or password is same or not
        Returns :
            True if password is verified
            Else False
        """
        if bcrypt.checkpw(password.encode(), hashed_password.encode()):
            return True

        return False

    async def list_users(self) -> list[User]:
        """
        List all the users
        """
        all_users = await self.user_repo.get_all()
        return all_users
