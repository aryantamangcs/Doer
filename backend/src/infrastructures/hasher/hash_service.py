import bcrypt


class Hasher:
    """
    List of hash conerning methods and attributes
    """

    def hash(self, value: str) -> str:
        """
        Hashes the values using bcrypt and returns the hashed value
        Args:
            value
        Returns:
            The hashed value
        """
        return bcrypt.hashpw(value.encode("utf-8"), bcrypt.gensalt()).decode()

    def verify(self, hashed_value: str, value: str) -> bool:
        """
        Verifies whether the hashed_value and the provided value are same
        Args:
            hashed_value
            value
        Returns:
            If they are same it returns True else it returns False
        """
        return bcrypt.checkpw(value.encode("utf-8"), hashed_value.encode("utf-8"))
