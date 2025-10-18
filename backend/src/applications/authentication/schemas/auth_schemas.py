from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, model_validator


class SignUpSchema(BaseModel):
    """
    Schema to validate the payload while signing up user
    """

    first_name: str = Field(
        ..., title="First name", description="First name of the user"
    )
    last_name: str = Field(..., title="Last name", description="Last name of the user")
    username: str = Field(
        ..., title="User name", description="The display name of the user"
    )
    email: EmailStr = Field(
        ..., title="Email address", description="Email address of the user"
    )
    password: str = Field(
        ...,
        title="Password",
        description="Minimum 8 character long password",
        min_length=8,
    )

    model_config = {"extra": "forbid"}


class LoginSchema(BaseModel):
    """
    Schema to validate the payload while logging in user
    """

    email: EmailStr = Field(
        ..., title="Email address", description="Email adress of the user"
    )
    password: str = Field(..., title="Password", description="Password of the user")

    model_config = {"extra": "forbid"}


class CheckUserCredentialsSchema(BaseModel):
    """
    Schema to validate the payload while checking user details
    """

    email: Optional[EmailStr] = Field(default=None, title="Email address")
    username: Optional[str] = Field(default=None, title="Username")

    @model_validator(mode="after")
    def check_payload(self):
        """
        Check if email and username both are provided
        If yes it raises error
        """

        if self.email and self.username:
            raise ValueError("Either email or username can be provided")

        return self


class TokenPayloadSchema(BaseModel):
    """
    Schema to include payload in tokens
    """

    first_name: str
    last_name: str
    username: str
    email: str
    identifier: str

    model_config = {"from_attributes": True}


class RefreshTokenSchema(BaseModel):
    """
    Schema to  validate payload in refresh token route
    """

    refresh_token: str = Field(..., title="Refresh token for new access token")


class UserOutSchema(BaseModel):
    """
    schema to validate payload while sending outside the application
    """

    first_name: str
    last_name: str
    username: str
    email: str
    identifier: str

    model_config = {"from_attributes": True}


class RefreshTokenSchema(BaseModel):
    """
    schema to validate refresh token
    """

    refresh_token: str
