from pydantic import BaseModel, Field


class CreateTodoListSchema(BaseModel):
    """
    schema to validate payload while creating todo list
    """

    name: str = Field(..., title="Name of the todo list")

    model_config = {"extra": "forbid"}
