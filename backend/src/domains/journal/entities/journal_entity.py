import uuid
from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class Journal:
    """
    Core attributes for Journal
    """

    created_by: int
    updated_at: datetime
    created_at: datetime
    title: str
    content: str
    identifier: str
    deleted_at: datetime | None = None

    id: int | None = None

    @classmethod
    def create(cls, title: str, content: str, created_by: int) -> Journal:
        """
        returns instance of Journal
        """
        return cls(
            title=title,
            content=content,
            created_by=created_by,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            identifier=str(uuid.uuid4()),
        )
