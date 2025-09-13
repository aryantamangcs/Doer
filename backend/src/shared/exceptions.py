import logging

from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

logger = logging.getLogger(__name__)


class DomainException(Exception):
    """
    Custom base domain  exception
    """

    def __init__(self, detail: str, data: str, status_code: int = HTTP_400_BAD_REQUEST):
        super().__init__(detail)
        logger.exception("%s (status_code = %d)", detail, status_code)
        self.status_code = status_code
        self.detail = detail
        self.data = data


class NotFoundError(DomainException):
    """
    Custom Exception for not found
    """

    def __init__(
        self,
        status_code: int = HTTP_404_NOT_FOUND,
        detail: str = "Not found Error",
        data: str | None = None,
    ):
        super().__init__(status_code=status_code, detail=detail, data=data)


class ConflictError(DomainException):
    """
    Exception for already exists
    """

    def __init__(
        self,
        status_code: int = HTTP_409_CONFLICT,
        detail: str = "Already exists",
        data: str | None = None,
    ):
        super().__init__(status_code=status_code, detail=detail, data=data)


class CreateError(DomainException):
    """
    Exception for create error
    """

    def __init__(
        self,
        status_code: int = HTTP_500_INTERNAL_SERVER_ERROR,
        detail: str = "Create error",
        data: str | None = None,
    ):
        super().__init__(status_code=status_code, detail=detail, data=data)


class InvalidError(DomainException):
    """
    Invalid error
    """

    def __init__(
        self,
        status_code: int = HTTP_400_BAD_REQUEST,
        detail: str = "Invalid error",
        data: str | None = None,
    ):
        super().__init__(status_code=status_code, detail=detail, data=data)


class ServerError(DomainException):
    """
    Server error
    """

    def __init__(
        self,
        status_code: int = HTTP_500_INTERNAL_SERVER_ERROR,
        detail: str = "Server error",
        data: str | None = None,
    ):
        super().__init__(status_code=status_code, detail=detail, data=data)
