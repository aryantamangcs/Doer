from typing import Callable

from sqlalchemy.ext.asyncio import AsyncSession

from infrastructures.authentication.mappers import to_entity, to_model
from src.domains.authentication.entities import User
from src.domains.authentication.repositories import UserRepo
from src.infrastructures.db.config import async_session

from ..models.user_model import UserModel


class UserRepoSqlAlchemy(UserRepo):
    """
    Implementation of Domain UserRepo
    """

    def __init__(self, session: Callable[[], AsyncSession]):
        self.get_session = session

    async def create(self, user: User) -> User:
        """
        Creates the user and returns the newly created user
        """
        async with self.get_session() as session:
            new_user = to_model(user)
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
            return to_entity(new_user)
