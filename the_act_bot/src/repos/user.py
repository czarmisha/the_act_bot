from uuid import UUID

from sqlalchemy import insert, select

from the_act_bot.src.database.models import User
from the_act_bot.src.schemas import user as schemas

from .base import SQLAlchemyRepo


class UserRepo(SQLAlchemyRepo):
    async def create(
        self, user_in: schemas.UserIn
    ) -> schemas.UserOut:
        stmt = (
            insert(User)
            .returning(User)
            .values(
                name=user_in.name,
                phone=user_in.phone,
                type=user_in.type,
                lang=user_in.lang,
            )
        )

        user = await self._session.scalar(stmt)

        await self._session.commit()
        return schemas.UserOut.model_validate(user)

    async def get_by_phone(self, phone: str) -> User:
        stmt = select(User).where(User.phone == phone)

        result = await self._session.scalar(stmt)

        if result is None:
            return

        return result

    async def get_by_id(self, user_id: UUID) -> User:
        stmt = select(User).where(User.id == user_id)

        result = await self._session.scalar(stmt)

        if result is None:
            return

        return result
