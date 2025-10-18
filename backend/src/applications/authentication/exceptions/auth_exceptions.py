from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_409_CONFLICT,
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from src.shared.exceptions import ConflictError, DomainError, InvalidError, ServerError


class CheckUserError(DomainError):
    """
    Check User Error
    """

    def __init__(
        self,
        detail: str = "Check User Error",
        data: str | None = None,
    ):
        super().__init__(detail=detail, data=data)


class EmailExistsError(ConflictError):
    """
    Email Already Exists error
    """

    def __init__(
        self,
        detail: str = "Email already exists",
        data: str | None = None,
    ):
        super().__init__(detail=detail, data=data)


class UsernameExistsError(ConflictError):
    """
    Username Already Exists error
    """

    def __init__(
        self,
        detail: str = "Username already exists",
        data: str | None = None,
    ):
        super().__init__(detail=detail, data=data)


class LoginInvalidError(InvalidError):
    """
    Invalid login credentials
    """

    def __init__(
        self,
        detail: str = "Invalid credentials",
        data: str | None = None,
    ):
        super().__init__(detail=detail, data=data)


class RefreshTokenError(ServerError):
    """
    RefreshToken Error
    """

    def __init__(
        self,
        detail: str = "Refresh Token Error",
        data: str | None = None,
    ):
        super().__init__(detail=detail, data=data)


class RefreshTokenInvalidError(DomainError):
    """
    RefreshToken Expired Error
    """

    def __init__(
        self,
        detail: str = "Refresh Token has expired",
    ):
        super().__init__(detail=detail, data=data)


class RefreshTokenExpiredError(DomainError):
    """
    RefreshToken Expired Error
    """

    def __init__(
        self,
        detail: str = "Refresh Token has expired",
    ):
        super().__init__(detail=detail, data=data)
