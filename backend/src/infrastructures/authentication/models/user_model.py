import uuid

from sqlalchemy import UUID
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from ..db.config import Base


class UserModel(Base):
    """
    User Model using SQLAlchemy
    """

    __tablename__ = "sys_users"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(length=50, nullable=False)
    last_name: Mapped[str] = mapped_column(length=50, nullable=False)
    email: Mapped[str] = mapped_column(length=50, nullable=False)
    password: Mapped[str] = mapped_column(length=50, nullable=False)
    identifier: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False
    )
    username: Mapped[str] = mapped_column(length=50, nullable=False)

    def __str__(self):
        return f"{self.email}"
