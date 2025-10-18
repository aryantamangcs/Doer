from datetime import datetime, timedelta
from typing import Any

import jwt

from src.infrastructures.config.settings import get_settings
from src.shared.exceptions import CreateError, InvalidError, UnAuthorizedError

settings = get_settings()


class TokenService:
    """
    List of token concern methods and services
    """

    @staticmethod
    def create_access_token(
        payload: dict[str, Any],
        expiry_minutes: int = settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES,
    ) -> str:
        """
        Creates access token using jwt

        Args :
            Payload (to be included in token)

        Return:
            new access token
        Raises:
            CreateError if any error while encoding access_token
        """
        try:
            expire = datetime.utcnow() + timedelta(minutes=expiry_minutes)
            payload["exp"] = expire
            access_token = jwt.encode(
                payload, settings.JWT_SECRET_KEY, algorithm="HS256"
            )
            return access_token

        except Exception as e:
            raise CreateError(
                detail="Error while creating jwt access token", data=str(e)
            ) from e

    @staticmethod
    def verify_access_token(token: str) -> dict[str, Any]:
        """
        Decodes access token and verifies it
        Args:
            token
        Returns:
            True if it is verified else False
        Raises:
            InvalidError if the provided token is invalid

        """
        try:
            decoded_token = jwt.decode(
                token, settings.JWT_SECRET_KEY, algorithms="HS256"
            )
            return decoded_token
        except Exception as e:
            raise UnAuthorizedError(detail="Error while decoding the jwt token") from e
