from abc import ABC, abstractmethod

from src.domains.journal.entities.journal_entity import Journal


class JournalRepository(ABC):
    """
    list of interfaces for journal repository
    """

    @abstractmethod
    async def add(self, journal: Journal) -> Journal:
        """
        creates the new journal
        """
        raise NotImplementedError

    @abstractmethod
    async def filter(self, where: dict | None = None, **kwargs) -> list[Journal]:
        """
        Finds item of todo on certain conditions
        """
        raise NotImplementedError
