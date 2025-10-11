from typing import Any

from fastapi.requests import Request
from fastapi.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.status import HTTP_400_BAD_REQUEST

from src.domains.authentication.entities.user_entity import User
from src.infrastructures.authentication.repository.user_repo_sqlalchemy import (
    UserRepoSqlAlchemy,
)
from src.infrastructures.common.context import current_user
from src.shared.exceptions import BearerTokenError, NotFoundError
from src.shared.response import CustomResponse as cr

from ..token.jwt_service import TokenService


class AuthMiddleware(BaseHTTPMiddleware):
    """
    list of methods and services for AuthMiddleware
    """

    def __init__(self, app, exclude_path: list[str | None] | None):
        super().__init__(app=app)
        self.exclude_path = exclude_path

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:

        try:
            if request.method.lower() == "options":
                return await call_next(request)

            exclude = await self.handle_exclude_path(request)
            if exclude:
                return await call_next(request)

            auth_token = request.headers.get("Authorization")
            if not auth_token:
                raise NotFoundError(detail="Authorization not found")
            token = await self.check_token_standard(auth_token)
            if not token:
                raise NotFoundError(detail="Token not found")

            user = await self.decode_token(token)

            # saving in request and in context
            request.state.user = user

            current_user.set(user)

            return await call_next(request)
        except Exception as e:  # pylint: disable=broad-except
            return cr.error(
                data=str(e),
                message=getattr(e, "detail", str(e)),
                status_code=getattr(e, "status_code", HTTP_400_BAD_REQUEST),
            )

    async def check_token_standard(self, token: str) -> str | None:
        """
        Check if the token standard is bearer or not
        """
        if token.split(" ", maxsplit=1)[0].lower() != "bearer":
            raise BearerTokenError()
        return token.split(" ", maxsplit=1)[1]

    async def decode_token(self, token: str) -> dict[str, Any]:
        """
        Decodes the token and returns the user details
        """
        details = TokenService.verify_access_token(token)
        user = await self.fetch_user_by_identifier(details["identifier"])
        if not user:
            raise NotFoundError(detail="Invalid token")
        return user.__dict__

    async def fetch_user_by_identifier(self, identifier: str) -> User:
        """
        Finds the user on the basis of identifier
        """

        user_repo = UserRepoSqlAlchemy()
        user = await user_repo.find_one(where={"identifier": identifier})
        if not user:
            raise NotFoundError(
                detail="User with that identifier not found",
            )
        return user

    async def handle_exclude_path(
        self,
        request: Request,
    ) -> bool:
        """
        Handles exclude path
        """
        if not self.exclude_path:
            return False

        if request.url.path in self.exclude_path:
            return True

        return False
