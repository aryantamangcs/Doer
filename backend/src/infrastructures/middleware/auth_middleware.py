from typing import Any

from fastapi.requests import Request
from fastapi.responses import JSONResponse, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN

from src.domains.authentication.entities.user_entity import User
from src.infrastructures.authentication.repository.user_repo_sqlalchemy import (
    UserRepoSqlAlchemy,
)
from src.infrastructures.common.context import current_user
from src.infrastructures.config.settings import get_settings
from src.infrastructures.exception_handler import DOMAIN_TO_HTTP
from src.shared.exceptions import BearerTokenError, NotFoundError, UnAuthorizedError
from src.shared.response import CustomResponse as cr

from ..token.jwt_service import TokenService

settings = get_settings()


class AuthMiddleware(BaseHTTPMiddleware):
    """
    list of methods and services for AuthMiddleware
    """

    def __init__(self, app, exclude_path: list[str | None] | None):
        super().__init__(app=app)
        self.exclude_path = exclude_path

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):

        origin = request.headers.get("origin")
        try:
            if request.method.lower() == "options":
                return await call_next(request)

            exclude = await self.handle_exclude_path(request)
            if exclude:
                return await call_next(request)

            auth_token = request.headers.get("Authorization")
            if not auth_token:
                raise UnAuthorizedError(detail="Authorization not found")
            token = await self.check_token_standard(auth_token)
            if not token:
                raise UnAuthorizedError(detail="Token not found")

            user = await self.decode_token(token)

            # saving in request and in context
            request.state.user = user

            current_user.set(user)

            return await call_next(request)
        except Exception as e:  # pylint: disable=broad-except
            return self.handle_unauthorized_response(origin, e)

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

    def handle_unauthorized_response(self, origin, e: Exception):
        """
        To avoid Access-Control-Allow-Origin problem
        """
        headers = {}

        if not origin in settings.ALLOW_ORIGINS:
            return cr.error(
                message="Origin not allowed", status_code=HTTP_403_FORBIDDEN
            )

        headers = {
            "Access-Control-Allow-Origin": origin,
            "Access-Control-Allow-Credentials": "true",
        }

        status_code = DOMAIN_TO_HTTP.get(getattr(e, "code"))
        return JSONResponse(
            status_code=status_code or HTTP_400_BAD_REQUEST,
            content={
                "data": str(e),
                "success": False,
                "message": getattr(e, "detail", str(e)),
            },
            headers=headers,
        )
