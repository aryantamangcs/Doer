from dataclasses import dataclass
from datetime import datetime


@dataclass
class Journal:
    """
    Core attributes for Journal
    """

    created_by: int
    date: datetime
    updated_at: datetime
    created_at: datetime
    title: str
    description: str
    identifier: str

    id: int | None


    @classmethod
    def create(cls,title:str,)


