from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, validates, relationship

import the_act_bot.src.database.enums as enums
import the_act_bot.src.database.models as models


class User(models.BaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    type: Mapped[enums.UserTypeEnums] = mapped_column(nullable=False)
    lang: Mapped[enums.LanguageEnums] = mapped_column(nullable=False)
    phone: Mapped[str] = mapped_column(index=True, nullable=False)
    name: Mapped[str | None]

    cart: Mapped["models.Cart"] = relationship("Cart", back_populates="user")
    payments: Mapped[list["models.Payment"]] = relationship("Payment", back_populates="user")

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
