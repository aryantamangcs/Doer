from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructures.common.models import BaseModel
from src.infrastructures.common.timestamp_mixin import TimeStampMixin


class TodoItemModel(BaseModel, TimeStampMixin):
    """
    Todo item model
    """

    __tablename__ = "todo_items"

    todo_list_id: Mapped[int] = mapped_column(
        ForeignKey("todo_lists.id"), on_delete="CASCADE", index=True
    )
    title: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey("sys_users.id"), index=True)
    identifier: Mapped[str] = mapped_column(nullable=False)
