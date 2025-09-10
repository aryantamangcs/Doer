from fastapi import APIRouter
from starlette.status import HTTP_201_CREATED

from src.shared.response import CustomResponse as cr
from src.shared.response import CustomResponseSchema

from ..schemas import SignUpSchema

router = APIRouter(prefix="/auth")


@router.post("/signup", response_model=CustomResponseSchema)
def signup(payload: SignUpSchema):
    """
    Registers the user and returns user info

    Args:
        All the fields in SignUpSchema

    Returns:
        JSON : with access_token and refresh_token

    Raises:
        SignUpError exception if any error occuurs while signing up user
    """

    return cr.success(
        message="Successfully signed up a user", status_code=HTTP_201_CREATED
    )
