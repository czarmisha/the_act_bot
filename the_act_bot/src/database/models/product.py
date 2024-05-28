from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

import the_act_bot.src.database.models as models


class Product(models.BaseModel):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[dict[str, str]] = mapped_column(MutableDict.as_mutable(JSONB()), nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)

    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    category: Mapped[models.Category] = relationship("Category", back_populates="products")
    image: Mapped[models.Image] = relationship("Image", back_populates="product")
