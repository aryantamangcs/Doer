from src.domains.journal.entities.journal_entity import Journal
from src.domains.journal.services.journal_domain_services import JournalDomainServices
from src.infrastructures.authentication.repository.user_repo_sqlalchemy import (
    UserRepoSqlAlchemy,
)
from src.infrastructures.common.context import current_user
from src.infrastructures.journal.repositories.journal_repo_sqlalchemy import (
    JournalRepositorySqlAlchemy,
)

from ..schemas.journal_schemas import CreateJournalSchema


class JournalServices:
    """
    journal services methods
    """

    def __init__(self, domain_service: JournalDomainServices):
        self.domain_service = domain_service

    async def create_journal(self, payload: CreateJournalSchema) -> Journal:
        """
        Creates new journal
        Args:
            CreateJournalSchema
        Return:
            new Journal
        """

        user = current_user.get()

        return await self.domain_service.create_journal(
            title=payload.title, content=payload.content, created_by=user["id"]
        )

    async def list_journals(self) -> list[Journal]:
        """
        Creates new journal
        Return:
            new Journal
        """

        user = current_user.get()
        return await self.domain_service.list_journal(user_id=user["id"])


def get_journal_service() -> JournalServices:
    """
    Returns instance of JournalService
    """

    journal_repo = JournalRepositorySqlAlchemy()
    user_repo = UserRepoSqlAlchemy()
    journal_domain_service = JournalDomainServices(
        repo=journal_repo, user_repo=user_repo
    )
    return JournalServices(domain_service=journal_domain_service)
