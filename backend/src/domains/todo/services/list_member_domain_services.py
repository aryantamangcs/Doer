from src.domains.todo.entities.todo_entity import ListMember
from src.domains.todo.enums.todo_enums import TodoListMemberRoleEnum
from src.domains.todo.repositories.list_member_repo import ListMemberRepo


class ListMemberServices:
    """
    list of methods and services
    """

    def __init__(self, repo: ListMemberRepo):
        self.repo = repo

    async def add_member(
        self,
        user_id: int,
        todo_list_id: int,
        role: TodoListMemberRoleEnum = TodoListMemberRoleEnum.MEMBER,
    ) -> ListMember:
        """
        adds member
        Args:
            user_id : user id to be added
            role : role of user
        """
        member = ListMember.create(
            user_id=user_id, todo_list_id=todo_list_id, role=role
        )
        return await self.repo.add(member)

    async def remove_member(self, user_id: int, todo_list_id: int):
        """
        removes the member
        Args:
            user_id : user id to be added
            role : role of user
        """
        member = await self.repo.find_one(
            where={"user_id": user_id, "todo_list_id": todo_list_id}
        )
        if not member:
            raise ValueError("Member not found")
        await self.repo.delete(member)
