from src.domains.journal.entities.journal_entity import Journal
from src.domains.journal.repositories.journal_repo import JournalRepository


class JournalDomainServices:
    """
    list of methods and services for journal
    """

    def __init__(self, repo: JournalRepository):
        self.repo = repo

    async def create_journal(
        self, title: str, description: str, created_by: int
    ) -> Journal:
        """
        Creates a new journal
        Args:
            title : title of the journal
            description : description of the journal or content
            created_by : owner of the journal
        Returns:
            newly created journal
        """
        new_journal = Journal.create(
            title=title, description=description, created_by=created_by
        )
        return await self.repo.add(new_journal)
