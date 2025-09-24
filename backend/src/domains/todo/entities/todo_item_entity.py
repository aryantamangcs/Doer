import uuid
from dataclasses import dataclass
from datetime import datetime

from ..enums import TodoStatusEnum


@dataclass
class TodoItem:
    """
    Todo Item
    """

    todo_list_id: int
    title: str
    status: TodoStatusEnum
    description: str
    owner_id: int
    created_at: datetime
    updated_at: datetime
    identifier: str  # uuid
    deleted_at: datetime | None = None
    id: int | None = None

    @classmethod
    def create(
        cls,
        todo_list_id: int,
        title: str,
        status: TodoStatusEnum,
        description: str,
        owner_id: int,
        identifier=str(uuid.uuid4()),
    ):
        """
        Creates the todo item
        """
        return cls(
            todo_list_id=todo_list_id,
            title=title,
            status=status,
            description=description,
            owner_id=owner_id,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            identifier=identifier,
        )

    def change_title(self, title: str) -> None:
        """
        change the title to the new title
        Args:
            title : new title of the todo_list
        Return:
            None
        """
        self.title = title
        self.updated_at = datetime.now()

    def change_status(self, status: TodoStatusEnum) -> None:
        """
        Changes the status of the todo item
        Args:
            status : New status
        Return:
            None
        """

        self.status = status
        self.updated_at = datetime.now()

    def delete(self) -> None:
        """
        Delete the todo item
        """

        self.deleted_at = datetime.now()
