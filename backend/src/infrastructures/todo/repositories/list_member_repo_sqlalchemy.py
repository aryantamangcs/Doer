from typing import Any, Callable

from sqlalchemy.ext.asyncio import AsyncSession

from src.domains.todo.entities.todo_entity import ListMember
from src.domains.todo.repositories.list_member_repo import ListMemberRepo
from src.infrastructures.db.config import async_session
from src.infrastructures.todo.models.todo_list_model import ListMemberModel


class ListMemberRepoSqlAlchemy(ListMemberRepo):
    """
    implementation of list member repo
    """

    def __init__(self, session: Callable[[], AsyncSession] = async_session):
        self.get_session = session

    async def add(self, member: ListMember) -> ListMember:
        """
        adds the member to  list member
        """
        async with self.get_session() as session:
            new_todo_list_member = ListMemberModel(
                todo_list_id=member.todo_list_id,
                user_id=member.user_id,
                role=member.role,
                access=member.access,
            )
            session.add(new_todo_list_member)
            await session.commit()
            await session.refresh(new_todo_list_member)
            member.id = new_todo_list_member.id
            return member

    async def find_one(self, where: dict[str, Any] | None, **kwargs) -> ListMember:
        """
        finds the list member
        """

    async def delete(self, member: ListMember):
        """
        deletes the member
        """
