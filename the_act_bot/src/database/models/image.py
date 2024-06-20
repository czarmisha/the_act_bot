from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

import the_act_bot.src.database.models as models


class Image(models.BaseModel):
    __tablename__ = "images"

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String(100), nullable=True)
    file_unique_id: Mapped[str] = mapped_column(String(100), nullable=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))

    product: Mapped["models.Product"] = relationship("Product", back_populates="images")
