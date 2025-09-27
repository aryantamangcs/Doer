from typing import Any

from src.domains.todo.entities.todo_entity import ListMember
from src.domains.todo.repositories.list_member_repo import ListMemberRepo


class ListMemberRepoSqlAlchemy(ListMemberRepo):
    """
    implementation of list member repo
    """

    async def add(self, member: ListMember) -> ListMember:
        """
        adds the member to  list member
        """

    async def find_one(self, where: dict[str, Any] | None, **kwargs) -> ListMember:
        """
        finds the list member
        """

    async def delete(self, member: ListMember):
        """
        deletes the member
        """
