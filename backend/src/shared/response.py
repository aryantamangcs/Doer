from typing import Any, Generic, List, Optional, TypeVar, Union

from fastapi import Response, status
from fastapi.responses import JSONResponse
from pydantic.generics import GenericModel
from starlette.status import HTTP_204_NO_CONTENT

T = TypeVar("T")


class CustomResponseSchema(GenericModel, Generic[T]):
    """
    Custom Response Schema for every api
    """

    success: bool
    data: Optional[Union[T, List[T]]]
    message: str


class CustomResponse:
    """
    list of customer Response methods
    """

    @staticmethod
    def success(
        data: Any = None,
        message: str = "Successful",
        status_code: int = status.HTTP_200_OK,
    ):
        """
        On sucess it returns the success=True with data and message
        """
        if status_code is HTTP_204_NO_CONTENT:
            return Response(status_code=status_code)
        if ":" in message:
            message = message.split(":")[1]
        content = {"success": True, "message": message, "data": data}
        return JSONResponse(status_code=status_code, content=content)

    @staticmethod
    def error(
        data: Optional[Any] = None,
        message: Optional[str] = "Unsuccessful",
        status_code: Optional[int] = status.HTTP_400_BAD_REQUEST,
    ):
        """
        On error it returns the success=False and with data and message
        """
        content = {"success": False, "message": message, "data": data}
        return JSONResponse(status_code=status_code, content=content)
