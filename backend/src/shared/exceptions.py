from typing import Optional

from src.shared.logger.ansi_logger import get_logger

logger = get_logger("doer")


class DomainError(Exception):
    """
    Custom base domain  exception
    """

    code: str = "domain_error"

    def __init__(
        self,
        detail: str,
        data: Optional[str] = None,
    ):
        super().__init__(detail)
        logger.exception("%s", detail)
        self.detail = detail
        self.data = data


class NotFoundError(DomainError):
    """
    Custom Exception for not found
    """

    code: str = "not_found"

    def __init__(
        self,
        detail: str = "Not found Error",
        data: str | None = None,
    ):
        super().__init__(detail=detail, data=data)


class ConflictError(DomainError):
    """
    Exception for already exists
    """

    code: str = "conflict_error"

    def __init__(
        self,
        detail: str = "Already exists",
        data: str | None = None,
    ):
        super().__init__(detail=detail, data=data)


class CreateError(DomainError):
    """
    Exception for create error
    """

    code: str = "create_error"

    def __init__(
        self,
        detail: str = "Create error",
        data: str | None = None,
    ):
        super().__init__(detail=detail, data=data)


class DeleteError(DomainError):
    """
    Exception for delete error
    """

    code: str = "delete_error"

    def __init__(
        self,
        detail: str = "Delete error",
        data: str | None = None,
    ):
        super().__init__(detail=detail, data=data)


class InvalidError(DomainError):
    """
    Invalid error
    """

    code: str = "invalid_error"

    def __init__(
        self,
        detail: str = "Invalid error",
        data: str | None = None,
    ):
        super().__init__(detail=detail, data=data)


class UnAuthorizedError(DomainError):
    """
    unauthorized error
    """

    code: str = "unauthorized_error"

    def __init__(
        self,
        detail: str = "Unauthorized error",
        data: str | None = None,
    ):
        super().__init__(detail=detail, data=data)


class ServerError(DomainError):
    """
    Server error
    """

    code: str = "server_error"

    def __init__(
        self,
        detail: str = "Server error",
        data: str | None = None,
    ):

        super().__init__(detail=detail, data=data)


class BearerTokenError(InvalidError):
    """
    BearerToken error
    """

    def __init__(
        self,
        detail: str = "The token standard is not Bearer",
        data: str | None = None,
    ):
        super().__init__(detail=detail, data=data)
