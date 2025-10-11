from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from ..config.settings import get_settings

settings = get_settings()

async_engine = create_async_engine(url=settings.ASYNC_DATABASE_URL, echo=False)
sync_engine = create_engine(url=settings.SYNC_DATABASE_URL, echo=False)

async_session = async_sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)


Base = declarative_base()
