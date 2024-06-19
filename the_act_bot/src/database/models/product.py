from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

import the_act_bot.src.database.models as models


class Product(models.BaseModel):  # TODO: variants?
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[dict[str, str]] = mapped_column(MutableDict.as_mutable(JSONB()), nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
    stock: Mapped[int] = mapped_column(nullable=False, default=0)
    discount_id: Mapped[int] = mapped_column(ForeignKey("discounts.id"), nullable=True)

    images: Mapped[list["models.Image"]] = relationship("Image", back_populates="product")
    discount: Mapped["models.Discount"] = relationship("Discount", back_populates="products")
    product_categories: Mapped[list["models.ProductCategory"]] = relationship(
        "Category", secondary="product_categories", back_populates="product"
    )


class ProductCategory(models.BaseModel):
    __tablename__ = "product_categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))

    product: Mapped["models.Product"] = relationship("Product")
    category: Mapped["models.Category"] = relationship("Category")

    __table_args__ = (UniqueConstraint("product_id", "category_id"),)
