class NotFoundError(Exception):
    """
    Custom Not Found error exception
    """


class ConflictError(Exception):
    """
    Exception for already exists
    """

    def __init__(self, detail: str):
        self.detail = detail
