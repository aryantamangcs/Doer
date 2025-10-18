from pydantic import BaseModel


class CreateJournalSchema(BaseModel):
    """
    schema to validate the payload while creating journal
    """

    title: str
    content: str


class CreateJournalOutSchema(BaseModel):
    """
    schema to validate the data while sending outside the application
    """

    identifier: str
    title: str

    model_config = {"from_attributes": True}


class JournalOutSchema(BaseModel):
    """
    schema to validate the data while sending outside the application
    """

    identifier: str
    title: str
    content: str

    model_config = {"from_attributes": True}
