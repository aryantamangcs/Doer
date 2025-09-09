from src.shared.exceptions import ConflictError

from ..entities import User
from ..repositories import UserRepo


class UserServices:
    """
    List of methods and attributes for UserServices
    """

    def __init__(self, user_repo: UserRepo):
        self.user_repo = user_repo

    async def create_user(self, user: User) -> User:
        """
        Creates user and returns the user
        """
        user_exists = await self.user_repo.get_by_email(user.email)
        if not user_exists:
            raise ConflictError(detail="User with this email already exists")
        new_user = await self.user_repo.create(user)
        return new_user

    async def list_users(self) -> list[User]:
        """
        List all the users
        """
        all_users = await self.user_repo.get_all()
        return all_users
