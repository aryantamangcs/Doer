from datetime import datetime
from unittest.mock import AsyncMock, Mock

import pytest

from src.domains.todo.entities.todo_entity import TodoList
from src.domains.todo.services import todo_list_domain_services
from src.domains.todo.services.list_member_domain_services import ListMemberServices
from src.domains.todo.services.todo_list_domain_services import TodoListDomainServices
from src.shared.exceptions import NotFoundError


@pytest.fixture
def todo_list_repo():
    """
    returns the mock instance of todo list repo
    """
    return AsyncMock()


@pytest.fixture
def user_repo():
    """
    returns the mock instance of User repo
    """
    return AsyncMock()


@pytest.fixture
def list_member_repo():
    """
    returns the mock instance of User repo
    """
    return AsyncMock()


@pytest.fixture
def list_member_service(list_member_repo):
    """
    list member service
    """
    return ListMemberServices(list_member_repo)


@pytest.fixture
def todo_list_domain_service(todo_list_repo, user_repo, list_member_repo):
    """
    returns an instance of todolist domain service
    """

    return TodoListDomainServices(todo_list_repo, user_repo, list_member_repo)


@pytest.mark.asyncio
async def test_create_todo_list(todo_list_domain_service):
    """
    test create todo list
    """
    todo_list_domain_service.repo.add.return_value = TodoList(
        name="test",
        created_at=datetime.now(),
        updated_at=datetime.now(),
        identifier="djfkajdfkajfdkdaljf",
        owner_id=0,
    )

    result = await todo_list_domain_service.create_todo_list("test", 0)
    assert isinstance(result, TodoList) is True


@pytest.mark.asyncio
async def test_list_all_todo_list(todo_list_domain_service):
    """
    test list all todo list
    """
    todo_list_domain_service.repo.filter.return_value = [
        TodoList(
            name="test",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            identifier="djfkajdfkajfdkdaljf",
            owner_id=0,
        )
    ]

    result = await todo_list_domain_service.list_all_todo_list(0)
    assert isinstance(result, list) is True


@pytest.mark.asyncio
async def test_delete_todo_list(todo_list_domain_service):
    """
    test delete todo list
    """

    todo_list_domain_service.repo.get_by_identifier = AsyncMock(
        return_value=TodoList(
            id=1,
            name="test",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            identifier="djfkajdfkajfdkdaljf",
            owner_id=0,
        )
    )

    result = await todo_list_domain_service.delete_todo_list(
        identifier="test_identifier"
    )
    assert result is None


@pytest.mark.asyncio
async def test_delete_todo_list_invalid_identifier(todo_list_domain_service):
    """
    test delete todo list invalid identifier
    """

    todo_list_domain_service.repo.get_by_identifier = AsyncMock(return_value=None)

    with pytest.raises(NotFoundError):
        await todo_list_domain_service.delete_todo_list(identifier="test_identifier")
