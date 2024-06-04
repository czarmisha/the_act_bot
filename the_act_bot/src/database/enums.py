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
