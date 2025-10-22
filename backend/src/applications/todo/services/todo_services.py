from datetime import date

from src.applications.todo.schemas.todo_schemas import (
    CreateTodoItemSchema,
    CreateTodoListMemberSchema,
    CreateTodoListSchema,
    EditTodoItemSchema,
    EditTodoListSchema,
    TodoListMemberSchema,
)
from src.domains.todo.entities.todo_entity import TodoList
from src.domains.todo.entities.todo_item_entity import TodoItem
from src.domains.todo.repositories.todo_item_repo import TodoItemRepository
from src.domains.todo.services.list_member_domain_services import ListMemberServices
from src.domains.todo.services.todo_item_domain_services import TodoItemDomainServices
from src.domains.todo.services.todo_list_domain_services import TodoListDomainServices
from src.infrastructures.authentication.repository.user_repo_sqlalchemy import (
    UserRepoSqlAlchemy,
)
from src.infrastructures.common.context import current_user
from src.infrastructures.todo.models.todo_list_model import (
    ListMemberModel,
    TodoListModel,
)
from src.infrastructures.todo.repositories.list_member_repo_sqlalchemy import (
    ListMemberRepoSqlAlchemy,
)
from src.infrastructures.todo.repositories.todo_item_repo_sqlalchemy import (
    TodoItemRepoSqlAlchemy,
)
from src.infrastructures.todo.repositories.todo_list_repo_sqlalchemy import (
    TodoListRepoSqlAlchemy,
)
from src.shared.exceptions import InvalidError, ServerError


class TodoServices:
    """
    list of methods and services for todo"""

    def __init__(
        self,
        todo_list_repo: TodoListRepoSqlAlchemy,
        todo_list_domain_services: TodoListDomainServices,
        todo_item_domain_services: TodoItemDomainServices,
    ):
        self.todo_list_repo = todo_list_repo
        self.todo_list_domain_services = todo_list_domain_services
        self.todo_item_domain_services = todo_item_domain_services

    async def create_todo_list(self, payload: CreateTodoListSchema) -> TodoList:
        """
        creates todo list
        Args:
            CreateTodoListSchema
        Return:
            newly created todolist
        """
        user = current_user.get()
        todo_list = await self.todo_list_domain_services.create_todo_list(
            name=payload.name, owner_id=user["id"]
        )
        return todo_list

    async def list_todos(self) -> list[TodoList]:
        """
        lists all the todo list
        """
        user = current_user.get()
        all_todo_lists = await self.todo_list_domain_services.list_all_todo_list(
            user_id=user["id"],
            related=[
                TodoListModel.members,
                (TodoListModel.members, ListMemberModel.member),
            ],
        )
        return all_todo_lists

    async def edit_todo_list(self, identifier: str, payload: EditTodoListSchema):
        """
        Edit todo item
        """
        updated_list = await self.todo_list_domain_services.edit_todo_list(
            identifier, payload.model_dump(exclude_none=True)
        )
        if not updated_list:
            raise ServerError(detail="Error while updating todo list")
        return updated_list

    async def delete_todo_list(self, identifier: str):
        """
        delete todo list
        """
        await self.todo_list_domain_services.delete_todo_list(identifier=identifier)

    async def create_todo_item(self, payload: CreateTodoItemSchema) -> TodoItem:
        """
        creates todo item
        Args:
            CreateTodoItemSchema
        Return:
            Newly created todo_item
        """
        user = current_user.get()
        new_todo_item = await self.todo_item_domain_services.create_todo_item(
            todo_list_identifier=payload.todo_list_identifier,
            title=payload.title,
            status=payload.status,
            description=payload.description,
            owner_id=user["id"],
        )
        return new_todo_item

    async def list_todo_items(
        self, todo_list_identifier: str, req_date: date | None
    ) -> list[TodoItem]:
        """
        lists all the todo items
        Returns:
            List of todo_items
        """
        return await self.todo_item_domain_services.list_todo_item_by_todo_list(
            todo_list_identifier, req_date
        )

    async def delete_todo_item(self, identifier: str):
        """
        delete todo item
        """
        await self.todo_item_domain_services.delete_todo_item(identifier=identifier)

    async def edit_todo_item(self, identifier: str, payload: EditTodoItemSchema):
        """
        Edit todo item
        """
        updated_item = await self.todo_item_domain_services.edit_todo_item(
            identifier, payload.model_dump(exclude_none=True)
        )
        if not updated_item:
            raise ServerError(detail="Error while updating todo item")
        return updated_item

    async def todo_list_add_member(self, payload: CreateTodoListMemberSchema):
        """
        adds member in todo list
        """
        member = await self.todo_list_domain_services.add_member(
            todo_list_identifier=payload.todo_list_identifier,
            user_identifier=payload.user_identifier,
        )
        if not member:
            raise ServerError(detail="Error while adding member")
        return member


def get_todo_services() -> TodoServices:
    """
    returnns an instance of TodoServices
    """
    todo_list_repo = TodoListRepoSqlAlchemy()
    todo_item_repo = TodoItemRepoSqlAlchemy()
    user_repo = UserRepoSqlAlchemy()
    list_member_repo = ListMemberRepoSqlAlchemy()
    list_member_service = ListMemberServices(repo=list_member_repo)
    todo_item_domain_services = TodoItemDomainServices(
        repo=todo_item_repo, todo_list_repo=todo_list_repo
    )
    todo_list_domain_services = TodoListDomainServices(
        repo=todo_list_repo,
        user_repo=user_repo,
        list_member_service=list_member_service,
    )
    return TodoServices(
        todo_list_repo=todo_list_repo,
        todo_list_domain_services=todo_list_domain_services,
        todo_item_domain_services=todo_item_domain_services,
    )
