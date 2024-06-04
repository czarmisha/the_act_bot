from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

import the_act_bot.src.database.models as models
import the_act_bot.src.database.enums as enums


class Discount(models.BaseModel):
    __tablename__ = "discounts"

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[enums.DiscountTypeEnums] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    value: Mapped[int] = mapped_column(nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    product: Mapped["models.Product"] = relationship("Product", back_populates="discounts")

    @validates("value")
    def validate_value(self, key, value):
        if value < 0:
            raise ValueError
        return value
