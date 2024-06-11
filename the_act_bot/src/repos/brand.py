from sqlalchemy import insert, select, update, delete

from the_act_bot.src.database import enums
from the_act_bot.src.database.models import Brand
from the_act_bot.src.schemas import brand as schemas

from .base import SQLAlchemyRepo


class BrandRepo(SQLAlchemyRepo):
    async def create(
        self, brand_in: schemas.BrandIn
    ) -> schemas.BrandOut:
        stmt = (
            insert(Brand)
            .returning(Brand)
            .values(
                name=brand_in.name,
                position=brand_in.position,
            )
        )

        brand = await self._session.scalar(stmt)

        await self._session.commit()
        return schemas.BrandOut.model_validate(brand)
    
    async def list(self) -> list[schemas.BrandOut]:
        query = select(Brand).order_by(Brand.position)
        brands = await self._session.scalars(query)

        return [schemas.BrandOut.model_validate(brand) for brand in brands]

    async def get_by_id(self, brand_id: int) -> Brand:
        stmt = select(Brand).where(Brand.id == brand_id)

        result = await self._session.scalar(stmt)

        if result is None:
            return

        return result
    
    async def update(self, id: int, brand_in: schemas.BrandIn):
        if not brand_in.model_dump(exclude_none=True):
            return True
        
        stmt = (
            update(Brand)
            .where(Brand.id == id)
            .values(**brand_in.model_dump(exclude_none=True))
        )

        await self._session.execute(stmt)
        await self._session.commit()

        return True
    
    async def remove(self, id: int):
        stmt = (
            delete(Brand)
            .where(Brand.id == id)
        )

        await self._session.execute(stmt)
        await self._session.commit()
