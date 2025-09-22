from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from starlette.status import (
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

from src.shared.exceptions import DomainError
from src.shared.response import CustomResponse as cr


async def global_exception_handler(request: Request, exc: Exception):
    """
    Handles the global exception with custom response
    """
    if isinstance(exc, RequestValidationError):
        status_code = HTTP_422_UNPROCESSABLE_ENTITY
        detail = exc.errors()

    if isinstance(exc, DomainError):
        status_code = exc.status_code
        detail = exc.detail
        data = exc.data

    else:
        status_code = HTTP_500_INTERNAL_SERVER_ERROR
        detail = str(exc)
        data = str(exc)
    return cr.error(status_code=status_code, message=detail, data=data)


def add_exceptions_handler(app: FastAPI):
    """
    Adds alll exception handlers to the application
    """
    app.add_exception_handler(RequestValidationError, global_exception_handler)
    app.add_exception_handler(DomainError, global_exception_handler)
