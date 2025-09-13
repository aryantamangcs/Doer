from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructures.db.config import Base


class TimeStampMixin(Base):  # pylint: disable=(too-few-public-methods)
    """
    Time Stamp Mixin with fields such as:
    - created_at
    - updated_at
    - deleted_at
    """

    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        onupdate=lambda: func.now(),
        nullable=True,
    )

    deleted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
