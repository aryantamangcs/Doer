import asyncio
import os

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.infrastructures.config.settings import get_settings

settings = get_settings()

import pytest_asyncio


@pytest_asyncio.fixture(scope="session", autouse=True)
async def db_setup():
    """
    db setup and migration
    """
    alembic_cfg = Config(os.path.join(os.path.dirname(__file__), "../alembic.ini"))
    alembic_cfg.set_main_option("sqlalchemy.url", settings.TEST_SYNC_DATABASE_URL)
    command.upgrade(alembic_cfg, "head")

    yield

    async_engine = create_async_engine(url=settings.TEST_ASYNC_DATABASE_URL, echo=False)
    async with async_engine.begin() as conn:
        await conn.execute(text("DROP SCHEMA public CASCADE"))
        await conn.execute(text("CREATE SCHEMA public"))
    await async_engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def db_session():
    """
    test db setup
    """

    async_engine = create_async_engine(url=settings.TEST_ASYNC_DATABASE_URL, echo=False)

    async_session = async_sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )

    return async_session
