from typing import Callable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.domains.journal.entities.journal_entity import Journal
from src.domains.journal.repositories.journal_repo import JournalRepository
from src.infrastructures.db.config import async_session
from src.infrastructures.journal.models.journal_model import JournalModel


class JournalRepositorySqlAlchemy(JournalRepository):
    """
    implementation of journal repository interfaces
    """

    def __init__(self, session: Callable[[], AsyncSession] = async_session):
        self.get_session = session

    async def add(self, journal: Journal) -> Journal:
        """
        adds the new journal to the model
        Returns:
            new journal
        """

        async with self.get_session() as session:
            new_journal = JournalModel(
                title=journal.title,
                content=journal.content,
                identifier=journal.identifier,
                created_by=journal.created_by,
            )
            session.add(new_journal)
            await session.commit()
            await session.refresh(new_journal)
            journal.id = new_journal.id
            return journal

    async def filter(
        self, where: dict | None = None, related: list[str] | None = None, **kwargs
    ) -> list[Journal]:
        """
        finds journal
        """

        query = select(JournalModel)
        if related:
            for rel in related:
                if isinstance(rel, tuple):
                    root_rel, nested_rel = rel
                    query = query.options(
                        selectinload(root_rel).selectinload(nested_rel)
                    )
                else:
                    # Simple relationship
                    query = query.options(selectinload(rel))

        if where:
            for attr, value in where.items():
                column = getattr(JournalModel, attr)
                query = query.where(column == value)

        async with self.get_session() as session:
            result = await session.execute(query)
            all_journals = result.scalars().unique().all()

            if not all_journals:
                return []
            data = [
                Journal(
                    id=journal.id,
                    created_at=journal.created_at,
                    updated_at=journal.updated_at,
                    identifier=journal.identifier,
                    created_by=journal.created_by,
                    deleted_at=journal.deleted_at,
                    title=journal.title,
                    content=journal.content,
                )
                for journal in all_journals
            ]
            return data
