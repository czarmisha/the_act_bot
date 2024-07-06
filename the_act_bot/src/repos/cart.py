from uuid import UUID

from sqlalchemy import insert, select, update

from the_act_bot.src.database import enums
from the_act_bot.src.database.models import Cart
from the_act_bot.src.schemas import cart as schemas

from .base import SQLAlchemyRepo


class CartRepo(SQLAlchemyRepo):
    async def create(
        self, cart_in: schemas.CartIn
    ) -> schemas.CartOut:
        stmt = (
            insert(Cart)
            .returning(Cart)
            .values(
                name=cart_in.name,
                telegram_id=cart_in.telegram_id,
                phone=cart_in.phone,
                type=cart_in.type,
                lang=cart_in.lang,
            )
        )

        cart = await self._session.scalar(stmt)

        await self._session.commit()
        return schemas.CartOut.model_validate(cart)
    
    async def is_admin(self, telegram_id: int) -> bool:
        stmt = select(Cart).where(Cart.telegram_id == telegram_id, Cart.type == enums.CartTypeEnums.ADMIN)

        result = await self._session.scalar(stmt)

        if result is None:
            return False

        return True

    async def get_by_phone(self, phone: str) -> Cart:
        stmt = select(Cart).where(Cart.phone == phone)

        result = await self._session.scalar(stmt)

        if result is None:
            return

        return result

    async def get_by_id(self, cart_id: int) -> Cart:
        stmt = select(Cart).where(Cart.id == cart_id)

        result = await self._session.scalar(stmt)

        if result is None:
            return

        return result
    
    async def get_by_telegram_id(self, telegram_id: int) -> Cart:
        stmt = select(Cart).where(Cart.telegram_id == telegram_id)

        result = await self._session.scalar(stmt)

        if result is None:
            return

        return result
    
    async def update(self, telegram_id: int ,cart_in: schemas.CartUpdate):
        stmt = (
            update(Cart)
            .where(Cart.telegram_id == telegram_id)
            .values(**cart_in.model_dump(exclude_none=True))
        )

        await self._session.execute(stmt)
        await self._session.commit()

        return True
