from src.applications.todo.schemas.todo_schemas import CreateTodoListSchema
from src.domains.todo.entities.todo_entity import TodoList
from src.domains.todo.services.list_member_domain_services import ListMemberServices
from src.domains.todo.services.todo_list_domain_services import TodoListDomainServices
from src.infrastructures.authentication.repository.user_repo_sqlalchemy import (
    UserRepoSqlAlchemy,
)
from src.infrastructures.common.context import current_user
from src.infrastructures.todo.repositories.list_member_repo_sqlalchemy import (
    ListMemberRepoSqlAlchemy,
)
from src.infrastructures.todo.repositories.todo_list_repo_sqlalchemy import (
    TodoListRepoSqlAlchemy,
)


class TodoServices:
    """
    list of methods and services for todo
    """

    def __init__(
        self,
        todo_list_repo: TodoListRepoSqlAlchemy,
        todo_list_domain_services: TodoListDomainServices,
    ):
        self.todo_list_repo = todo_list_repo
        self.todo_list_domain_services = todo_list_domain_services

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
            name=payload.name, owner_id=user.id
        )
        return todo_list


def get_todo_services() -> TodoServices:
    """
    returnns an instance of TodoServices
    """
    todo_list_repo = TodoListRepoSqlAlchemy()
    user_repo = UserRepoSqlAlchemy()
    list_member_repo = ListMemberRepoSqlAlchemy()
    list_member_service = ListMemberServices(repo=list_member_repo)
    todo_list_domain_services = TodoListDomainServices(
        repo=todo_list_repo,
        user_repo=user_repo,
        list_member_service=list_member_service,
    )
    return TodoServices(
        todo_list_repo=todo_list_repo,
        todo_list_domain_services=todo_list_domain_services,
    )
