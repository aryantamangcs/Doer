from starlette.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_409_CONFLICT,
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from src.shared.exceptions import ConflictError, DomainError, InvalidError


class CheckUserError(DomainError):
    """
    Check User Error
    """

    def __init__(
        self,
        detail: str = "Check User Error",
        data: str | None = None,
        status_code: int = HTTP_422_UNPROCESSABLE_ENTITY,
    ):
        super().__init__(status_code=status_code, detail=detail, data=data)


class EmailExistsError(ConflictError):
    """
    Email Already Exists error
    """

    def __init__(
        self,
        detail: str = "Email already exists",
        data: str | None = None,
        status_code: int = HTTP_409_CONFLICT,
    ):
        super().__init__(status_code=status_code, detail=detail, data=data)


class UsernameExistsError(ConflictError):
    """
    Username Already Exists error
    """

    def __init__(
        self,
        detail: str = "Username already exists",
        data: str | None = None,
        status_code: int = HTTP_409_CONFLICT,
    ):
        super().__init__(status_code=status_code, detail=detail, data=data)


class LoginInvalidError(InvalidError):
    """
    Invalid login credentials
    """

    def __init__(
        self,
        detail: str = "Invalid credentials",
        data: str | None = None,
        status_code: int = HTTP_400_BAD_REQUEST,
    ):
        super().__init__(status_code=status_code, detail=detail, data=data)


class RefreshTokenError(DomainError):
    """
    RefreshToken Error
    """

    def __init__(
        self,
        detail: str = "Refresh Token Error",
        data: str | None = None,
        status_code: int = HTTP_500_INTERNAL_SERVER_ERROR,
    ):
        super().__init__(status_code=status_code, detail=detail, data=data)
