from typing import Any

from src.domains.authentication.repositories.user_repository import UserRepo
from src.domains.todo.services.list_member_domain_services import ListMemberServices
from src.shared.exceptions import CreateError, DeleteError, NotFoundError, ServerError

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
        try:
            data = await self.repo.add(todo_list=new_todo_list)
            return data
        except Exception as e:
            raise CreateError(
                detail="Error while creating todo list", data=str(e)
            ) from e

    async def list_all_todo_list(self) -> list[TodoList]:
        """
        Lists all the todo lists
        """
        return await self.repo.filter()

    async def delete_todo_list(self, identifier: str):
        """
        delete the todo list by id
        """
        todo_list = await self.repo.get_by_identifier(identifier=identifier)
        if not todo_list:
            raise NotFoundError(detail="Todo list not found")
        if not todo_list.id:
            raise ServerError(detail="Todo list id is None")

        try:
            await self.repo.delete(id=todo_list.id)
        except Exception as e:
            raise DeleteError() from e

    async def add_member(
        self, todo_list_identifier: str, user_identifier: str
    ) -> ListMember:
        """
        Adds member to the new_todo_list
        Args:
            user_id to be added
        """
        todo_list = await self.repo.get_by_identifier(todo_list_identifier)
        if not todo_list:
            raise NotFoundError(detail="Todo list not found")
        if not todo_list.id:
            raise ServerError(detail="Todo list id is none")

        new_member = await self.user_repo.get_by_identifier(user_identifier)
        if not new_member:
            raise NotFoundError(detail="Member to be added not found")
        if not new_member.id:
            raise ServerError(detail="Member is set to none")

        new_list_member = await self.list_member_service.add_member(
            user_id=new_member.id, todo_list_id=todo_list.id
        )
        return new_list_member

    async def delete_member(
        self, todo_list_identifier: str, user_identifier: str
    ) -> None:
        """
        Adds member to the new_todo_list
        Args:
            user_id to be deleted
        """
        todo_list = await self.repo.get_by_identifier(todo_list_identifier)
        if not todo_list:
            raise NotFoundError(detail="Todo list not found")
        if not todo_list.id:
            raise ServerError(detail="Todo list id is none")

        member = await self.user_repo.get_by_identifier(user_identifier)
        if not member:
            raise NotFoundError("Member to be deleted not found")
        if not member.id:
            raise ServerError(detail="Member id is set to none")

        await self.list_member_service.remove_member(
            user_id=member.id, todo_list_id=todo_list.id
        )
        await self.repo.update(todo_list)

    async def edit_todo_list(
        self, todo_list_identifier: str, payload: dict[str, Any]
    ) -> TodoList | None:
        """
        Edits the todo list details
        Args:
            todo list identifier
            payload
        Returns:
            Newly updated todo_list or None

        """

        todo_list = await self.repo.get_by_identifier(todo_list_identifier)
        if not todo_list:
            raise NotFoundError(detail="Todo list not found")
        if not todo_list.id:
            raise ServerError(detail="todo list id is set none")

        for keys in payload.keys():
            match keys:
                case "name":
                    todo_list.change_name(name=payload["name"])
                case _:
                    return None

        updated_list = await self.repo.update(todo_list)
        return updated_list
