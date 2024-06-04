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

    image: Mapped["models.Image"] = relationship("Image", back_populates="product")
    discount: Mapped["models.Discount"] = relationship("Discount", back_populates="product")
    product_categories: Mapped[list["models.ProductCategory"]] = relationship(
        "ProductCategory", back_populates="product"
    )


class ProductCategory(models.BaseModel):
    __tablename__ = "product_categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))

    product: Mapped["models.Product"] = relationship("Product", back_populates="product_categories")
    category: Mapped["models.Category"] = relationship("Category", back_populates="products")

    __table_args__ = (UniqueConstraint("product_id", "category_id"),)
