from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

import the_act_bot.src.database.models as models



class Cart(models.BaseModel):
    __tablename__ = "carts"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user: Mapped["models.User"] = relationship("User", back_populates="cart", single_parent=True, foreign_keys=[user_id])
    items: Mapped[list["CartItem"]] = relationship("CartItem", back_populates="cart")

    __table_args__ = (UniqueConstraint("user_id"),)


class CartItem(models.BaseModel):
    __tablename__ = "cart_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    cart_id: Mapped[int] = mapped_column(ForeignKey("carts.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))

    cart: Mapped["Cart"] = relationship("Cart", back_populates="items")
    product: Mapped["models.Product"] = relationship("Product")
