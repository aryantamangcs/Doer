from uuid import UUID

from src.domains.authentication.entities import User, UserData

from .models.user_model import UserModel


def to_model(user: User) -> UserModel:
    """Maps User to UserModel"""
    return UserModel(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        identifier=user.identifier,
        password=user.password,
        username=user.username,
    )


def to_entity(user: UserModel) -> User:
    """Maps User to UserModel"""
    user_data = UserData(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        identifier=user.identifier,
        password=user.password,
        username=user.username,
    )

    return User(user_data=user_data)
