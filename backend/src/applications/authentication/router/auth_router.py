import logging

from fastapi import APIRouter, Depends, Query
from fastapi.requests import Request
from pydantic import EmailStr
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from src.applications.authentication.schemas.auth_schemas import (
    LoginSchema,
    RefreshTokenSchema,
    UserOutSchema,
)
from src.infrastructures.common.context import current_user
from src.shared.response import CustomResponse as cr
from src.shared.response import CustomResponseSchema

from ..schemas import SignUpSchema
from ..services.auth_services import get_auth_services

router = APIRouter(prefix="/auth", tags=["Auth"])

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


@router.get("/all-users", response_model=CustomResponseSchema)
async def get_all_users(auth_service=Depends(get_auth_services)):
    """
    Get all the users
    """
    all_users = await auth_service.list_all_users()
    return cr.success(
        message="Successfully fetched all users",
        data=[UserOutSchema.model_validate(user).model_dump() for user in all_users],
    )


@router.get("/refresh-token", response_model=CustomResponseSchema)
async def refresh_token_fetch(
    refresh_token: str = Query(..., title="Refresh token to fetch new access token"),
    auth_service=Depends(get_auth_services),
):
    """
    Fetches the access token from the provided Refresh token in Authorization Header with Bearere Standard

    Returns :
        JSON : with new access_token

    Raises :
        RefreshTokenExpiredError if the refresh token has expired
        InvalidRefreshTokenError if the provided refresh token is not valid
    """
    user = current_user.get()

    payload = await auth_service.validate_refresh_token(refresh_token, user)

    return cr.success(
        message="Successfully refetched refresh token",
        data=payload,
        status_code=HTTP_200_OK,
    )


@router.get("/check-user", response_model=CustomResponseSchema)
async def check_user(
    email: EmailStr = Query(
        None, description="Email to check whether it exists or not"
    ),
    username: str = Query(
        None, description="Username to check whether it exists or not"
    ),
    auth_service=Depends(get_auth_services),
):
    """
    Checks whether there is any conflict error
    """
    value = await auth_service.check_user_credentials(email=email, username=username)
    return cr.success(message=f"{value} is available")
