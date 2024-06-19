from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

import the_act_bot.src.database.models as models

class Category(models.BaseModel):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[dict[str, str]] = mapped_column(MutableDict.as_mutable(JSONB()), nullable=False)
    position: Mapped[int] = mapped_column(nullable=False, default=1)
    active: Mapped[bool] = mapped_column(nullable=False, default=True)
    brand_id: Mapped[int] = mapped_column(ForeignKey("brands.id"))

    product_categories: Mapped[list["models.ProductCategory"]] = relationship(
        "Product", secondary="product_categories", back_populates="category", cascade="all, delete"
    )
    brand: Mapped["models.Brand"] = relationship("Brand", back_populates="categories")

    __table_args__ = (UniqueConstraint("name", "brand_id"),)
