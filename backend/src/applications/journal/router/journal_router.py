import logging

from fastapi import APIRouter, Depends
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from src.applications.journal.schemas.journal_schemas import (
    CreateJournalOutSchema,
    CreateJournalSchema,
    JournalOutSchema,
)
from src.applications.journal.services.journal_services import get_journal_service
from src.shared.response import CustomResponse as cr
from src.shared.response import CustomResponseSchema

router = APIRouter(prefix="/journal", tags=["Journal"])

logger = logging.getLogger("doer_logger")


@router.post("/journal", response_model=CustomResponseSchema)
async def create_journal(
    payload: CreateJournalSchema, journal_service=Depends(get_journal_service)
):
    """
    Creates a new journal
    Args:
        All the fields in CreateJournalSchema
    Returns:
        JSON : with newly created journal title and identifier
    """
    data = await journal_service.create_journal(payload)

    return cr.success(
        message="Successfully created your journal",
        status_code=HTTP_201_CREATED,
        data=CreateJournalOutSchema.model_validate(data).model_dump(),
    )


@router.get("/journal/{user_identifier:str}", response_model=CustomResponseSchema)
async def list_journal(
    user_identifier: str, journal_service=Depends(get_journal_service)
):
    """
    Creates a new journal
    Args:
        user_identifier : str
    Returns:
        JSON : with all journal associated with the given user
    """
    data = await journal_service.list_journals(user_identifier)

    return cr.success(
        message="Successfully listed your journall",
        status_code=HTTP_200_OK,
        data=[
            JournalOutSchema.model_validate(journal).model_dump() for journal in data
        ],
    )
