from pydantic import BaseModel, EmailStr, Field


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
