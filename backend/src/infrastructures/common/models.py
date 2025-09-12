from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructures.db.config import Base


class BaseModel(Base):  # pylint: disable=(too-few-public-methods)
    """
    Base Model for all the models
    This model consists of simply id,
    If you need other basic field then you have to use Mixins

    """

    id: Mapped[int] = mapped_column(primary_key=True, index=True, nullable=False)
