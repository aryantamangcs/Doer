import logging

from fastapi import APIRouter, Depends
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from src.applications.authentication.schemas.auth_schemas import LoginSchema
from src.infrastructures.authentication.models import refresh_token_model
from src.shared.response import CustomResponse as cr
from src.shared.response import CustomResponseSchema

from ..schemas import SignUpSchema
from ..services.auth_services import get_auth_services

router = APIRouter(prefix="/auth")

logger = logging.getLogger("doer_logger")


@router.post("/signup", response_model=CustomResponseSchema)
async def signup(
    payload: SignUpSchema,
    auth_service=Depends(get_auth_services),
):
    """
    Registers the user and returns user info

    Args:
        All the fields in SignUpSchema

    Returns:
        JSON : with access_token and refresh_token

    Raises:
        SignUpError exception if any error occuurs while signing up user
    """
    data = await auth_service.create_user(payload)

    return cr.success(
        message="Successfully signed up a user", status_code=HTTP_201_CREATED, data=data
    )


@router.post("/login", response_model=CustomResponseSchema)
async def login(payload: LoginSchema, auth_service=Depends(get_auth_services)):
    """
    Checks the provided credentials and returns user info

    Args:
        All the fields in LoginSchema

    Returns:
        JSON: with access token and refresth token
    """
    data = await auth_service.validate_credentials(payload)
    return cr.success(
        message="Successfully logged in", status_code=HTTP_200_OK, data=data
    )


@router.post("/refresh-token", response_model=CustomResponseSchema)
def refresh_token():
    """
    Fetches the access token from the provided Refresh token in Authorization Header with Bearere Standard

    Returns :
        JSON : with new access_token

    Raises :
        RefreshTokenExpiredError if the refresh token has expired
        InvalidRefreshTokenError if the provided refresh token is not valid
    """
