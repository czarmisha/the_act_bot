import enum


class UserTypeEnums(str, enum.Enum):
    USER = "user"
    ADMIN = "admin"
    SYSTEM = "system"


class LanguageEnums(str, enum.Enum):
    EN = "en"
    RU = "ru"
    UZ = "uz"


class DiscountTypeEnums(str, enum.Enum):
    FIXED = "fixed"
    PERCENT = "percent"
    PROMO = "promo"


class OrderStatusEnums(str, enum.Enum):
    NEW = "new"
    PAYED = "payed"
    CANCELED = "canceled"
    COMPLETED = "completed"


class PaymentMethodEnums(str, enum.Enum):
    CASH = "cash"
    CLICK = "click"
    PAYME = "payme"
    UZUM = "uzum"
