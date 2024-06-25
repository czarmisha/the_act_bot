from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

import the_act_bot.src.database.models as models


class Image(models.BaseModel):
    __tablename__ = "images"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_file_path: Mapped[str] = mapped_column(String(100), nullable=True)
    tg_file_unique_id: Mapped[str] = mapped_column(String(100), nullable=True)
    tg_file_id: Mapped[str] = mapped_column(nullable=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"))

    product: Mapped["models.Product"] = relationship("Product", back_populates="images")
