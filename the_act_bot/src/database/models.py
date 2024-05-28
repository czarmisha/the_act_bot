from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, UniqueConstraint, func
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, validates, relationship

from the_act_bot.src.database.enums import LanguageEnums, UserTypeEnums


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


class User(BaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    type: Mapped[UserTypeEnums] = mapped_column(UserTypeEnums, nullable=False)
    lang: Mapped[LanguageEnums] = mapped_column(LanguageEnums, nullable=False)
    phone: Mapped[str] = mapped_column(index=True, nullable=False)
    name: Mapped[str | None]

    cart: Mapped["Cart"] = relationship("Cart", back_populates="user")
    payments: Mapped[list["Payment"]] = relationship("Payment", back_populates="user")

    @validates("phone")
    def validate_phone(self, key, value):
        if key == "phone":
            if not value:
                raise ValueError("Phone number is required")
            if not value[1:].isdigit():
                raise ValueError("Phone number must be a number")
            if len(value) != 13:
                raise ValueError("Phone number must be 12 characters long")
            if value[:4] != "+998":
                raise ValueError("Phone number must start with +998")
        return value
    

class Brand(BaseModel):
    __tablename__ = "brands"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    categories: Mapped[list["Category"]] = relationship("Category", back_populates="brand")


class Category(BaseModel):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[dict[str, str]] = mapped_column(MutableDict.as_mutable(JSONB()), nullable=False)
    brand_id: Mapped[int] = mapped_column(ForeignKey("brands.id"))

    products: Mapped[list["Product"]] = relationship("Product", back_populates="category")

    __table_args__ = (UniqueConstraint("name", "brand_id"),)


class Product(BaseModel):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[dict[str, str]] = mapped_column(MutableDict.as_mutable(JSONB()), nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)

    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    category: Mapped["Category"] = relationship("Category", back_populates="products")
    image: Mapped["Image"] = relationship("Image", back_populates="product")


class Image(BaseModel):
    __tablename__ = "images"

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String(100), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))

    product: Mapped["Product"] = relationship("Product", back_populates="images")


class Cart(BaseModel):
    __tablename__ = "carts"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user: Mapped["User"] = relationship("User", back_populates="cart", single_parent=True)
    items: Mapped[list["CartItem"]] = relationship("CartItem", back_populates="cart")

    __table_args__ = (UniqueConstraint("user_id"),)


class CartItem(BaseModel):
    __tablename__ = "cart_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    cart_id: Mapped[int] = mapped_column(ForeignKey("carts.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))

    cart: Mapped["Cart"] = relationship("Cart", back_populates="items")
    product: Mapped["Product"] = relationship("Product")


class Payment(BaseModel):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user: Mapped["User"] = relationship("User", back_populates="payments")


class Order(BaseModel):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user: Mapped["User"] = relationship("User", back_populates="orders")
    items: Mapped[list["OrderItem"]] = relationship("OrderItem", back_populates="order")


class OrderItem(BaseModel):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))

    order: Mapped["Order"] = relationship("Order", back_populates="items")
    product: Mapped["Product"] = relationship("Product")
