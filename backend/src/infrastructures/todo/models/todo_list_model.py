from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructures.authentication.models.user_model import UserModel
from src.infrastructures.common.models import BaseModel
from src.infrastructures.common.timestamp_mixin import TimeStampMixin


class ListMemberModel(BaseModel):
    """
    Todo list entity sqlalchemy implementation
    """

    __tablename__ = "todo_list_members"

    todo_list_id: Mapped[int] = mapped_column(ForeignKey("todo_lists.id"), index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("sys_users.id"))

    role: Mapped[str] = mapped_column(nullable=False)
    joined_at: Mapped[datetime] = mapped_column(default=datetime.now)

    joined_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # relationships
    todo_list: Mapped["TodoListModel"] = relationship(back_populates="members")


class TodoListModel(BaseModel, TimeStampMixin):
    """
    Todo list entity sqlalchemy implementation
    """

    __tablename__ = "todo_lists"

    name: Mapped[str] = mapped_column(nullable=False)
    identifier: Mapped[str] = mapped_column(nullable=False, index=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("sys_users.id"), index=True)
    members: Mapped[list[ListMemberModel]] = relationship(back_populates="todo_list")

    # relationships
    owner: Mapped[UserModel] = relationship(back_populates="todo_lists")
