import uuid
from datetime import datetime
from typing import Any

from src.applications.authentication.mappers import UserMapper
from src.applications.authentication.schemas.auth_schemas import (
    LoginSchema,
    SignUpSchema,
    TokenPayloadSchema,
)
from src.applications.authentication.services.token_services import TokenService
from src.domains.authentication.repositories import UserRepo
from src.domains.authentication.services import UserServices
from src.infrastructures.authentication.mappers import to_model
from src.infrastructures.authentication.models.refresh_token_model import (
    RefreshTokenModel,
)
from src.infrastructures.authentication.repository.refresh_token_sqlalchemy_repo import (
    RefreshTokenRepoSQLAchemy,
)
from src.infrastructures.authentication.repository.user_repo_sqlalchemy import (
    UserRepoSqlAlchemy,
)
from src.infrastructures.config.settings import get_settings
from src.shared.exceptions import ConflictError, CreateError, InvalidError, ServerError

settings = get_settings()


class AuthServices:
    """
    List of authentication concerning services and methods
    """

    def __init__(self, repo: UserRepo, refresh_token_repo: RefreshTokenRepoSQLAchemy):
        """
        Sets up repository and domain services
        """
        self.repo = repo
        self.refresh_token_repo = refresh_token_repo
        self.domain_serivce = UserServices(repo)

    async def create_user(self, payload: SignUpSchema) -> dict[str, Any]:
        """
        Creates user
        Returns :
            Newly created user
        Raises:
            ConflictError if email and username already exists
        """
        email_exists = await self.domain_serivce.check_email_already_exists(
            payload.email
        )
        username_exists = await self.domain_serivce.check_username_already_exists(
            payload.username
        )

        if email_exists:
            raise ConflictError(detail="User with this email already exists.")
        if username_exists:
            raise ConflictError(detail="User with this username already exists.")

        identifier = uuid.uuid4()  # every user is assigned a unique idenitifer
        user = UserMapper.to_domain(payload, identifier)
        user.password = self.domain_serivce.hash_password(user.password)
        user = await self.repo.create(user)
        user_model = to_model(user)

        user_details = TokenPayloadSchema.model_validate(
            user_model, from_attributes=True
        )
        user_details.identifier = str(user_details.identifier)
        access_token, refresh_token = self.get_access_refresh_token(
            user_details.model_dump(exclude={"id"})
        )

        await self.save_refresh_token(refresh_token, user_id=user_details.id)
        return {"access_token": access_token, "refresh_token": refresh_token}

    async def validate_credentials(self, payload: LoginSchema) -> dict[str, Any]:
        """
        Validates the login credentials
        Returns:
            Access token and refresh token
        """
        user = await self.repo.get_by_email(payload.email)
        if not user:
            raise InvalidError(detail="Invalid credentials")
        verified = await self.domain_serivce.verify_password(
            user.password, payload.password
        )
        if not verified:
            raise InvalidError(detail="Invalid credentials")

        user_model = to_model(user)

        user_details = TokenPayloadSchema.model_validate(
            user_model, from_attributes=True
        )
        user_details.identifier = str(user_details.identifier)

        token = self.get_access_refresh_token(user_details.model_dump(exclude={"id"}))
        refresh_token = await self.refresh_token_repo.get_refresh_token_by_user(user.id)

        if not refresh_token:
            raise ServerError(detail="Error while fetching refresh token")

        return {"access_token": token[0], "refresh_token": refresh_token}

    def get_access_refresh_token(self, payload: dict[str, Any]) -> tuple[str, str]:
        """
        Processes the access token and refresh token
        Returns
         access token and refresh token with tuple packing
        """

        access_token = TokenService.create_access_token(payload)
        refresh_token = TokenService.create_access_token(
            {"id": payload["identifier"]},
            expiry_minutes=settings.JWT_REFRESH_TOKEN_EXPIRE_MINUTES,
        )
        return access_token, refresh_token

    async def save_refresh_token(self, token: str, user_id: int):
        """
        Saves refresh token in the db
        """

        try:
            data = TokenService.verify_access_token(token)
        except Exception as e:
            raise InvalidError(
                detail="Error while decoding the access token", data=str(e)
            ) from e

        expire_datetime = datetime.fromtimestamp(data["exp"])

        refresh_token = RefreshTokenModel(
            user_id=user_id, refresh_token=token, expires_at=expire_datetime
        )
        try:
            await self.refresh_token_repo.create(refresh_token)
        except Exception as e:
            raise CreateError(detail="Error while creating refresh token") from e


def get_auth_services() -> AuthServices:
    """
    Returns an instaance of Auth services
    """

    repo = UserRepoSqlAlchemy()
    refresh_token_repo = RefreshTokenRepoSQLAchemy()
    return AuthServices(repo, refresh_token_repo)
