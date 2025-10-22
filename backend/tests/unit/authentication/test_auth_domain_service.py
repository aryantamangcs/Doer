from unittest.mock import AsyncMock, Mock

import pytest

from src.domains.authentication.entities.user_entity import User
from src.domains.authentication.services.user_services import UserServices


@pytest.fixture
def user_repo():
    """
    returns the reusable mock instance
    """
    return AsyncMock()


@pytest.fixture
def auth_service(user_repo):
    """
    returns instance of UserServices
    """
    return UserServices(user_repo=user_repo)


@pytest.fixture
def hasher():
    """
    returns the hasher of
    """
    return Mock()


@pytest.mark.asyncio
async def test_email_already_exists_returns_true(auth_service):
    """
    tests email already_exists returns true
    """
    auth_service.user_repo.get_by_email.return_value = User(
        id=1,
        email="test@gmail.com",
        first_name="test",
        last_name="test",
        username="test",
        identifier="dfjakljdfaf",
        _password="test",
    )

    result = await auth_service.check_email_already_exists("test@gmail.com")
    assert result is True


@pytest.mark.asyncio
async def test_email_already_exists_returns_false(auth_service):
    """
    test email already exists return false
    """

    auth_service.user_repo.get_by_email.return_value = None

    result = await auth_service.check_email_already_exists("test@gmail.com")
    assert result is False


@pytest.mark.asyncio
async def test_check_username_already_exists_true(auth_service):
    """
    test  check username already exists true
    """

    auth_service.user_repo.get_by_username.return_value = User(
        id=1,
        email="test@gmail.com",
        first_name="test",
        last_name="test",
        username="test",
        identifier="dfjakljdfaf",
        _password="test",
    )

    result = await auth_service.check_username_already_exists("test")
    assert result is True


@pytest.mark.asyncio
async def test_check_username_already_exists_false(auth_service):
    """
    test  check username already exists false
    """

    auth_service.user_repo.get_by_username.return_value = None

    result = await auth_service.check_username_already_exists("test")
    assert result is False


def test_hash_password(auth_service, hasher):
    """
    test hash password
    """
    hasher.hash.return_value = "hashed value"
    result = auth_service.hash_password("test_password", hasher)

    assert isinstance(result, str) is True


def test_verify_password_returns_true(auth_service, hasher):
    """
    test verify password returns true
    """

    hasher.verify.return_value = True

    result = auth_service.verify_password("hashed_password", "test_password", hasher)
    assert result is True


def test_verify_password_returns_false(auth_service, hasher):
    """
    test verify password returns false
    """

    hasher.verify.return_value = False

    result = auth_service.verify_password("hashed_password", "test_password", hasher)
    assert result is False


@pytest.mark.asyncio
async def test_list_all_users(auth_service):
    """
    test list all users
    """

    auth_service.user_repo.filter = AsyncMock(
        return_value=[
            User(
                id=1,
                email="test@gmail.com",
                first_name="test",
                last_name="test",
                username="test",
                identifier="dfjakljdfaf",
                _password="test",
            )
        ]
    )

    result = await auth_service.list_all_users()

    assert isinstance(result, list) is True
