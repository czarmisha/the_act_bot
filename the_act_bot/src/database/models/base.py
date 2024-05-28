from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseModel(DeclarativeBase):
    """An abstract base model that adds created_at and updated_at timestamp fields to the model"""

    __abstract__ = True

    created: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=func.now(),
        server_default="now()",
        server_onupdate="now()",
        index=True,
    )
    updated: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=func.now(),
        server_default="now()",
        server_onupdate="now()",
        onupdate=func.now(),
    )

    def __repr__(self):
        return f"{self.__tablename__}: {getattr(self, 'id', '')} \n\t{self.created}\n\t{self.updated}"  # noqa

    def __str__(self):
        return self.__repr__()
