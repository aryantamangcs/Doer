from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructures.common.models import BaseModel
from src.infrastructures.common.timestamp_mixin import TimeStampMixin


class JournalModel(BaseModel, TimeStampMixin):
    """
    Journal entity implmenetation using sqlalchemy
    """

    __tablename__ = "sys_journal"

    title: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_by: Mapped[int] = mapped_column(
        ForeignKey("sys_users.id", ondelete="CASCADE"), index=True
    )
    identifier: Mapped[str] = mapped_column(nullable=False, index=True)
