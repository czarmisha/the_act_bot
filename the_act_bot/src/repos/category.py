import typing
from sqlalchemy import insert, select, update, delete

from the_act_bot.src.database.models import Category
from the_act_bot.src.schemas import category as schemas

from .base import SQLAlchemyRepo


class CategoryRepo(SQLAlchemyRepo):
    async def create(
        self, category_in: schemas.CategoryIn
    ) -> schemas.CategoryOut:
        stmt = (
            insert(Category)
            .returning(Category)
            .values(
                name=category_in.name,
                position=category_in.position,
                brand_id=category_in.brand_id,
            )
        )

        category = await self._session.scalar(stmt)

        await self._session.commit()
        return schemas.CategoryOut.model_validate(category)
    
    async def list(self) -> typing.List[schemas.CategoryOut]:
        query = select(Category).order_by(Category.position)
        categories = await self._session.scalars(query)

        return [schemas.CategoryOut.model_validate(category) for category in categories]
    

    async def list_by_brand_id(self, id: int) -> typing.List[schemas.CategoryOut]:
        query = select(Category).where(Category.brand_id == id).order_by(Category.position)
        categories = await self._session.scalars(query)

        return [schemas.CategoryOut.model_validate(category) for category in categories]
    

    async def get_by_id(self, category_id: int) -> Category:
        stmt = select(Category).where(Category.id == category_id)

        result = await self._session.scalar(stmt)

        if result is None:
            return

        return result
    
    async def update(self, id: int, category_in: schemas.Category):
        if not category_in.model_dump(exclude_none=True):
            return True
        
        stmt = (
            update(Category)
            .where(Category.id == id)
            .values(**category_in.model_dump(exclude_none=True))
        )

        await self._session.execute(stmt)
        await self._session.commit()

        return True
    
    async def remove(self, id: int):
        stmt = (
            delete(Category)
            .where(Category.id == id)
        )

        await self._session.execute(stmt)
        await self._session.commit()
