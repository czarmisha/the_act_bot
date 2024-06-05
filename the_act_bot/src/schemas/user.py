from pydantic import BaseModel, ConfigDict

from the_act_bot.src.database.enums import LanguageEnums, UserTypeEnums


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str | None = None
    telegram_id: int
    type: UserTypeEnums = UserTypeEnums.USER
    lang: LanguageEnums | None = None
    phone: str | None = None


class UserIn(User):
    pass


class UserOut(User):
    id: int
