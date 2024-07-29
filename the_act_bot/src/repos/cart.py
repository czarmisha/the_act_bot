from sqlalchemy import insert, select
from sqlalchemy.orm import selectinload
from sqlalchemy.dialects.postgresql import insert as pg_insert


from the_act_bot.src.database.models import Cart
from the_act_bot.src.database.models.cart import CartItem
from the_act_bot.src.schemas import cart as schemas

from .base import SQLAlchemyRepo


class CartRepo(SQLAlchemyRepo):
    async def create(
        self, user_id: int
    ) -> schemas.CartOut:
        stmt = (
            insert(Cart)
            .returning(Cart)
            .values(
                user_id=user_id
            )
        )

        cart = await self._session.scalar(stmt)

        await self._session.commit()
        return await schemas.CartOut.model_validate(cart)

    async def get_by_id(self, cart_id: int) -> Cart:
        stmt = select(Cart).where(Cart.id == cart_id)

        result = await self._session.scalar(stmt)

        if result is None:
            return

        return result

    async def get_info(self, cart_id: int) -> CartItem:
        stmt = select(CartItem).where(CartItem.cart_id == cart_id).options(
            selectinload(CartItem.product)
        )

        result = await self._session.scalars(stmt)

        if result is None:
            return

        return result.all()

    async def get_by_user_id(self, user_id: int) -> Cart:
        stmt = select(Cart).where(Cart.user_id == user_id)

        result = await self._session.scalar(stmt)

        if result is None:
            return

        return result

    async def add_item(
        self, cart_id: int, product_id: int, quantity: int
    ) -> schemas.CartItem:
        stmt = (
            pg_insert(CartItem)
            .values(
                cart_id=cart_id,
                product_id=product_id,
                quantity=quantity
            )
            .on_conflict_do_update(
                index_elements=[CartItem.cart_id, CartItem.product_id],
                set_={"quantity": CartItem.quantity + quantity}
            )
            .returning(CartItem)
        )

        cart_item = await self._session.scalar(stmt)

        await self._session.commit()
        return cart_item
