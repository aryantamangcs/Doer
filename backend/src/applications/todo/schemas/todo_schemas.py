from pydantic import BaseModel, ConfigDict, Field


class CreateTodoListSchema(BaseModel):
    """
    schema to validate payload while creating todo list
    """

    name: str = Field(..., title="Name of the todo list")

    model_config = ConfigDict(extra="forbid")
