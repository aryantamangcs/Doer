from src.domains.authentication.repositories.user_repository import UserRepo
from src.domains.todo.services.list_member_domain_services import ListMemberServices

from ..entities.todo_entity import ListMember, TodoList
from ..repositories.todo_list_repo import TodoListRepository


class TodoListDomainServices:
    """
    List of methods and services for todo list
    """

    def __init__(
        self,
        repo: TodoListRepository,
        user_repo: UserRepo,
        list_member_service: ListMemberServices,
    ):
        self.repo = repo
        self.user_repo = user_repo
        self.list_member_service = list_member_service

    async def create_todo_list(self, name: str, owner_id: int) -> TodoList:
        """
        Creates the todo list
        """
        new_todo_list = TodoList.create(name=name, owner_id=owner_id)
        return await self.repo.add(todo_list=new_todo_list)

    async def add_member(self, todo_list_id: int, user_id: int) -> ListMember:
        """
        Adds member to the new_todo_list
        Args:
            user_id to be added
        """
        todo_list = await self.repo.get_by_id(id=todo_list_id)
        if not todo_list:
            raise ValueError("Todo list not found")
        if not todo_list.id:
            raise ValueError("Todo list id is none")

        new_member = self.user_repo.get_by_id(id=user_id)
        if not new_member:
            raise ValueError("Member to be added not found")

        new_list_member = await self.list_member_service.add_member(
            user_id=user_id, todo_list_id=todo_list.id
        )
        return new_list_member

    async def delete_member(self, todo_list_id: int, user_id: int) -> None:
        """
        Adds member to the new_todo_list
        Args:
            user_id to be deleted
        """
        todo_list = await self.repo.get_by_id(id=todo_list_id)
        if not todo_list:
            raise ValueError("Todo list not found")
        if not todo_list.id:
            raise ValueError("Todo list id is none")

        new_member = self.user_repo.get_by_id(id=user_id)
        if not new_member:
            raise ValueError("Member to be deleted not found")

        await self.list_member_service.remove_member(
            user_id=user_id, todo_list_id=todo_list.id
        )
        await self.repo.update(todo_list)
