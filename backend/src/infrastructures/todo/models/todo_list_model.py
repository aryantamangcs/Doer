from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructures.common.models import BaseModel
from src.infrastructures.common.timestamp_mixin import TimeStampMixin


class ListMemberModel(BaseModel, TimeStampMixin):
    """
    Todo list entity sqlalchemy implementation
    """

    __tablename__ = "todo_list_members"

    todo_list_id: Mapped[int] = mapped_column(ForeignKey("todo_lists.id"), index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("sys_users.id"))

    role: Mapped[str] = mapped_column(nullable=False)
    access: Mapped[str] = mapped_column(nullable=False)

    # relationships
    todo_list: Mapped["TodoListModel"] = relationship(back_populates="members")
    member: Mapped["UserModel"] = relationship(back_populates="todo_list_member")


class TodoListModel(BaseModel, TimeStampMixin):
    """
    Todo list entity sqlalchemy implementation
    """

    __tablename__ = "todo_lists"

    name: Mapped[str] = mapped_column(nullable=False)
    identifier: Mapped[str] = mapped_column(nullable=False, index=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("sys_users.id"), index=True)

    # relationships
    members: Mapped[list[ListMemberModel]] = relationship(back_populates="todo_list")
    owner: Mapped["UserModel"] = relationship(back_populates="todo_lists")
