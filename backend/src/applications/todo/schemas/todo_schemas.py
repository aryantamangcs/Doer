from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_serializer


class CreateTodoListSchema(BaseModel):
    """
    schema to validate payload while creating todo list
    """

    name: str = Field(..., title="Name of the todo list")

    model_config = ConfigDict(extra="forbid")


class CreateTodoItemSchema(BaseModel):
    """
    schema to validate payload while creating todo item
    """

    title: str = Field(..., title="Title of the todo item")
    status: str = Field(..., title="Status of the todo item")
    description: str = Field(..., title="Description of the todo item")


class TodoListOutSchema(BaseModel):
    """
    schema to validate payload while sending outside the application
    """

    name: str
    created_at: datetime
    identifier: str
    owner_id: int

    @field_serializer("created_at")
    def datetime_serializer(self, value):
        """
        converts datetime into string
        """
        return value.isoformat()

    model_config = {"from_attributes": True}
