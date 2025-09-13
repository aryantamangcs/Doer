from typing import Callable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructures.db.config import async_session

from ..models.refresh_token_model import RefreshTokenModel


class RefreshTokenRepoSQLAchemy:
    """
    Refresh token repository pattern
    """

    def __init__(self, session: Callable[[], AsyncSession] = async_session):
        self.get_session = session

    async def create(self, refresh_token: RefreshTokenModel):
        """
        Creates the refresh token record
        """

        async with self.get_session() as session:
            session.add(refresh_token)
            await session.commit()
            await session.refresh(refresh_token)
            return refresh_token

    async def get_refresh_token_by_user(self, user_id: int | None) -> str | None:
        """
        Returns the refresh token by email
        """

        if not user_id:
            return None
        async with self.get_session() as session:
            stmt = select(RefreshTokenModel).where(RefreshTokenModel.user_id == user_id)
            result = await session.scalar(stmt)
            if result:
                return result.refresh_token
            return None
