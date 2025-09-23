from typing import Callable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domains.authentication.entities import User
from src.domains.authentication.repositories import UserRepo
from src.infrastructures.db.config import async_session

from ..models.user_model import UserModel


class UserRepoSqlAlchemy(UserRepo):
    """
    Implementation of Domain UserRepo
    """

    def __init__(self, session: Callable[[], AsyncSession] = async_session):
        self.get_session = session

    async def add(self, user: User) -> User:
        """
        adds the user and returns the newly created user
        """
        async with self.get_session() as session:
            new_user = UserModel(
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                password=user._password,
                identifier=user.identifier,
                username=user.username,
            )
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
            user.id = new_user.id
            return user

    async def find_one(self, where, **kwargs) -> User | None:
        """
        Finds user
        Returns:
            User if found else None
        """
        query = select(UserModel)
        if not where:
            raise ValueError("Where is missing")

        for attr, value in where.items():
            column = getattr(UserModel, attr)
            query = query.where(column == value)

        async with self.get_session() as session:
            result = await session.execute(query)
            user = result.scalar()

            if not user:
                return None
            return User(
                id=user.id,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                _password=user.password,
                username=user.username,
                identifier=str(user.identifier),
            )

    async def filter(self, **kwargs) -> list[User]:
        """
        Finds  list of users
        Returns:
            List of users
        """

    async def get_all(self, **kwargs) -> list[User]:
        """
        Finds  list of users
        Returns:
            List of users
        """

    async def update(self, user: User, **kwargs) -> User:
        """
        Finds user
        Returns:
            Update users
        """

    async def delete(self, **kwargs) -> None:
        """
        Deletes the user
        """

    async def get_by_email(self, email: str) -> User | None:
        """
        Gets user by email if exists
        Returns :
            User if found by email else returns None
        """
        async with self.get_session() as session:
            stmt = select(UserModel).where(UserModel.email == email)
            result = await session.scalar(stmt)
            if not result:
                return None

            user = User(
                id=result.id,
                first_name=result.first_name,
                last_name=result.last_name,
                email=result.email,
                _password=result.password,
                identifier=str(result.identifier),
                username=result.username,
            )
            return user

    async def get_by_username(self, username: str) -> User | None:
        """
        Gets user by username if exists
        Returns :
            User if found by username else returns None
        """
        async with self.get_session() as session:
            stmt = select(UserModel).where(UserModel.username == username)
            result = await session.scalar(stmt)

            if not result:
                return None

            user = User(
                id=result.id,
                first_name=result.first_name,
                last_name=result.last_name,
                email=result.email,
                _password=result.password,
                identifier=str(result.identifier),
                username=result.username,
            )
            return user
