import uuid

from sqlalchemy import UUID, String
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructures.common.models import BaseModel
from src.infrastructures.common.timestamp_mixin import TimeStampMixin
from src.infrastructures.todo.models.todo_list_model import TodoListModel


class UserModel(BaseModel, TimeStampMixin):
    """
    User Model using SQLAlchemy
    """

    __tablename__ = "sys_users"
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(50), nullable=False)
    password: Mapped[str] = mapped_column(String(50), nullable=False)
    identifier: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False
    )
    username: Mapped[str] = mapped_column(String(50), nullable=False)

    # relationships
    todo_lists: Mapped[list[TodoListModel]] = relationship(back_populates="owner")

    def __str__(self):
        return f"{self.email}"

    @property
    def user_id(self):
        """
        Returns the uuser_id
        """
        return self.id
