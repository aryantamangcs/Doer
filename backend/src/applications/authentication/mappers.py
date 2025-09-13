import uuid
from uuid import UUID

from src.applications.authentication.schemas.auth_schemas import SignUpSchema
from src.domains.authentication.entities.user_entity import User, UserData


class UserMapper:
    """
    list of mapper methods fo User
    """

    @staticmethod
    def to_domain(payload: SignUpSchema, identifier: UUID) -> User:
        """
        Converts schema data to domain entity
        """
        user_data = UserData(
            first_name=payload.first_name,
            last_name=payload.last_name,
            email=payload.email,
            identifier=identifier,
            password=payload.password,
            username=payload.username,
        )
        return User(user_data=user_data)
