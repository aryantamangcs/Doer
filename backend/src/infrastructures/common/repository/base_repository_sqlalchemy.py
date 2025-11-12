from typing import Generic, TypeVar

from src.domains.shared.base_domain_repository import BaseDomainRepository

T = TypeVar("T")


class BaseDomainRepositorySqlAlchemy(BaseDomainRepository[T]):
    """
    sqlalchemy implementation of base domain repository
    """
