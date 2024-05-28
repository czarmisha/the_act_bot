from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

import the_act_bot.src.database.models as models


class Brand(models.BaseModel):
    __tablename__ = "brands"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    categories: Mapped[list[models.Category]] = relationship("Category", back_populates="brand")
