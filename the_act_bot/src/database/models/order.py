from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

import the_act_bot.src.database.models as models
import the_act_bot.src.database.enums as enums


class Order(models.BaseModel):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    payment_method: Mapped[enums.PaymentMethodEnums] = mapped_column(nullable=False, default=enums.PaymentMethodEnums.CASH)
    status: Mapped[enums.OrderStatusEnums] = mapped_column(nullable=False, default=enums.OrderStatusEnums.NEW)

    user: Mapped["models.User"] = relationship("User", back_populates="orders", foreign_keys=[user_id])
    items: Mapped[list["OrderItem"]] = relationship("OrderItem", back_populates="order")


class OrderItem(models.BaseModel):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))

    order: Mapped["Order"] = relationship("Order", back_populates="items")
    product: Mapped["models.Product"] = relationship("Product")
