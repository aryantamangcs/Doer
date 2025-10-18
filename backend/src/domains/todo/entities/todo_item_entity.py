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
            identifier=str(uuid.uuid4()),
        )

    def change_title(self, title: str) -> None:
        """
        change the title to the new title
        Args:
            title : new title of the todo_item
        Return:
            None
        """
        self.title = title
        self.updated_at = datetime.now()

    def change_description(self, description: str) -> None:
        """
        change description to the new description
        Args:
            description: new description of todo_item
        Return:
            None
        """
        self.description = description
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

    def change_owner(self, owner_id: int) -> None:
        """
        Changes the owner of the todo item
        Args:
            owner_id : New owner id
        Return:
            None
        """
        self.owner_id = owner_id
        self.updated_at = datetime.now()

    def delete(self) -> None:
        """
        Delete the todo item
        """

        self.deleted_at = datetime.now()
