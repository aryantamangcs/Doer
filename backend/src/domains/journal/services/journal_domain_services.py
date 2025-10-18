from src.domains.authentication.repositories.user_repository import UserRepo
from src.domains.journal.entities.journal_entity import Journal
from src.domains.journal.repositories.journal_repo import JournalRepository
from src.shared.exceptions import NotFoundError, ServerError


class JournalDomainServices:
    """
    list of methods and services for journal
    """

    def __init__(self, repo: JournalRepository, user_repo: UserRepo):
        self.repo = repo
        self.user_repo = user_repo

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

    async def list_journal(self, user_identifier: str) -> list[Journal]:
        """
        List all the journal of the user
        Finds user by the public identifier
        then finds the jounral associated with the user
        """

        user = await self.user_repo.get_by_identifier(user_identifier)
        if not user:
            raise NotFoundError(detail="User not found")
        if not user.id:
            raise ServerError(detail="User id is set none")

        all_journals = await self.repo.filter(where={"created_by": user.id})
        return all_journals
