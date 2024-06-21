import typing
from sqlalchemy import insert, select, update, delete
from sqlalchemy.dialects.postgresql import insert as postgres_insert

from the_act_bot.src.database.models import Product, ProductCategory
from the_act_bot.src.schemas import product as schemas

from .base import SQLAlchemyRepo


class ProductRepo(SQLAlchemyRepo):
    async def create(
        self, product_in: schemas.ProductIn
    ) -> schemas.ProductOut:
        stmt = (
            insert(Product)
            .returning(Product)
            .values(
                name=product_in.name,
                description=product_in.description,
                stock=product_in.stock,
                price=product_in.price,
            )
        )

        product = await self._session.scalar(stmt)

        await self._session.commit()
        return schemas.ProductOut.model_validate(product)
    
    async def list(self) -> typing.List[schemas.ProductOut]:
        query = select(Product).order_by(Product.position)
        products = await self._session.scalars(query)

        return [schemas.ProductOut.model_validate(product) for product in products]

    async def get_by_id(self, product_id: int) -> Product:
        stmt = select(Product).where(Product.id == product_id)

        result = await self._session.scalar(stmt)

        if result is None:
            return

        return result
    
    async def add_category(self, product_id: int, category_id: int):
        stmt = postgres_insert(ProductCategory).values(
            product_id=product_id,
            category_id=category_id
        ).on_conflict_do_update(
            constraint='product_categories_pkey',
            set_=dict(product_id=product_id, category_id=category_id)
        )

        await self._session.execute(stmt)
        await self._session.commit()
    
    async def update(self, id: int, product_in: schemas.ProductIn):
        if not product_in.model_dump(exclude_none=True):
            return True
        
        stmt = (
            update(Product)
            .where(Product.id == id)
            .values(**product_in.model_dump(exclude_none=True))
        )

        await self._session.execute(stmt)
        await self._session.commit()

        return True
    
    async def remove(self, id: int):
        stmt = (
            delete(Product)
            .where(Product.id == id)
        )

        await self._session.execute(stmt)
        await self._session.commit()
    
    async def get_by_category_id(self, category_id: int) -> typing.List[schemas.ProductOut]:
        stmt = select(Product).join(ProductCategory).where(ProductCategory.category_id == category_id)
        products = await self._session.scalars(stmt)

        return [schemas.ProductOut.model_validate(product) for product in products]
