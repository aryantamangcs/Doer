from enum import Enum


class TodoStatusEnum(str, Enum):
    """
    TodoStatus Enum
    """

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class TodoListMemberRoleEnum(str, Enum):
    """
    TodoList member role
    """

    ADMIN = "admin"
    MEMBER = "member"
