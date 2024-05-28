from pydantic import BaseModel, ConfigDict

from the_act_bot.src.database.enums import LanguageEnums, UserTypeEnums


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str | None
    type: UserTypeEnums
    lang: LanguageEnums
    phone: str


class UserIn(User):
    pass


class UserOut(User):
    id: int
