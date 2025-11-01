import pytest
import pytest_asyncio

from src.applications.authentication.exceptions.auth_exceptions import (
    EmailExistsError,
    UsernameExistsError,
)
from src.applications.authentication.schemas.auth_schemas import (
    LoginSchema,
    SignUpSchema,
)
from src.applications.authentication.services.auth_services import AuthServices
from src.domains.authentication.services.user_services import UserServices
from src.infrastructures.authentication.repository.refresh_token_sqlalchemy_repo import (
    RefreshTokenRepoSQLAchemy,
)
from src.infrastructures.authentication.repository.user_repo_sqlalchemy import (
    UserRepoSqlAlchemy,
)
from src.infrastructures.hasher.hash_service import Hasher
from src.shared.exceptions import InvalidError
from tests.conftest import db_session


@pytest_asyncio.fixture(scope="function")
async def auth_service(db_session):
    """
    returns an instance of auth_service
    """

    async_session = db_session
    user_test_repo = UserRepoSqlAlchemy(async_session)
    refresh_token_repo = RefreshTokenRepoSQLAchemy(async_session)

    return AuthServices(
        repo=user_test_repo, refresh_token_repo=refresh_token_repo, hasher=Hasher()
    )


@pytest.mark.asyncio
async def test_auth_create(auth_service):
    """
    test create user
    """

    payload = SignUpSchema(
        first_name="test",
        last_name="test",
        email="test@gmail.com",
        username="test123",
        password="test12345",
    )

    result = await auth_service.create_user(payload)

    assert isinstance(result, dict) is True
    assert result.get("access_token", None) is not None
    assert result.get("refresh_token", None) is not None


@pytest.mark.asyncio
async def test_auth_create_email_exists_exception(auth_service):
    """
    test create user email exists
    """

    payload = SignUpSchema(
        first_name="test",
        last_name="test",
        email="test@gmail.com",
        username="test1234",
        password="test12345",
    )

    with pytest.raises(EmailExistsError):
        await auth_service.create_user(payload)


@pytest.mark.asyncio
async def test_auth_create_username_exists_exception(auth_service):
    """
    test create username exists
    """

    payload = SignUpSchema(
        first_name="test",
        last_name="test",
        email="test2@gmail.com",
        username="test123",
        password="test12345",
    )

    with pytest.raises(UsernameExistsError):
        await auth_service.create_user(payload)


@pytest.mark.asyncio
async def test_auth_validate_credentials(auth_service):
    """
    test create user
    """

    payload = LoginSchema(
        email="test@gmail.com",
        password="test12345",
    )

    result = await auth_service.validate_credentials(payload)

    assert isinstance(result, dict) is True
    assert result.get("access_token", None) is not None
    assert result.get("refresh_token", None) is not None


@pytest.mark.asyncio
async def test_auth_validate_credentials_wrong_email(auth_service):
    """
    test create user
    """

    payload = LoginSchema(
        email="test12@gmail.com",
        password="test12345",
    )

    with pytest.raises(InvalidError):
        await auth_service.validate_credentials(payload)


@pytest.mark.asyncio
async def test_auth_validate_credentials_wrong_password(auth_service):
    """
    test create user
    """

    payload = LoginSchema(
        email="test@gmail.com",
        password="test123456",
    )

    with pytest.raises(InvalidError):
        await auth_service.validate_credentials(payload)


@pytest.mark.asyncio
async def test_get_access_refresh_token_success(auth_service):
    """
    test get access refresh token
    """

    payload = {
        "identifier": "testedlfa",
        "name": "test",
    }

    result = auth_service.get_access_refresh_token(payload)

    assert isinstance(result, tuple) is True
    assert len(result) == 2


@pytest.mark.asyncio
async def test_get_access_refresh_token_failure(auth_service):
    """
    test get access refresh token
    """

    payload = {
        "name": "test",
    }

    with pytest.raises(KeyError):
        auth_service.get_access_refresh_token(payload)


@pytest.mark.asyncio
async def test_save_refresh_token_failure(auth_service):
    """
    test save refresh token failure
    """

    with pytest.raises(InvalidError):
        await auth_service.save_refresh_token(token="kkdalfjalkjfalf", user_id=1)


@pytest.mark.asyncio
async def test_check_user_credentials_providing_old_email(auth_service):
    """
    test check user credentials by providing already existing email
    """

    with pytest.raises(EmailExistsError):
        await auth_service.check_user_credentials(email="test@gmail.com")


@pytest.mark.asyncio
async def test_check_user_credentials_providing_new_email(auth_service):
    """
    test check user credentials by providing already existing email
    """

    email = await auth_service.check_user_credentials(email="testnew@gmail.com")
    assert isinstance(email, str) is True
    assert email == "testnew@gmail.com"


@pytest.mark.asyncio
async def test_check_user_credentials_providing_old_username(auth_service):
    """
    test check user credentials by providing already existing email
    """

    with pytest.raises(UsernameExistsError):
        await auth_service.check_user_credentials(username="test123")


@pytest.mark.asyncio
async def test_check_user_credentials_providing_new_username(auth_service):
    """
    test check user credentials by providing already existing username
    """

    username = await auth_service.check_user_credentials(username="test12345")
    assert isinstance(username, str) is True
    assert username == "test12345"
