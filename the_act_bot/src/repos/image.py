import typing
from sqlalchemy import insert, select, update, delete

from the_act_bot.src.database.models import Image
from the_act_bot.src.schemas import image as schemas

from .base import SQLAlchemyRepo


class ImageRepo(SQLAlchemyRepo):
    async def create(
        self, image_in: schemas.ImageIn
    ) -> schemas.ImageOut:
        stmt = (
            insert(Image)
            .returning(Image)
            .values(**image_in.model_dump(exclude_none=True))
        )

        image = await self._session.scalar(stmt)

        await self._session.commit()
        return schemas.ImageOut.model_validate(image)
    
    async def list(self) -> typing.List[schemas.ImageOut]:
        query = select(Image).order_by(Image.position)
        images = await self._session.scalars(query)

        return [schemas.ImageOut.model_validate(image) for image in images]

    async def get_by_id(self, image_id: int) -> Image:
        stmt = select(Image).where(Image.id == image_id)

        result = await self._session.scalar(stmt)

        if result is None:
            return

        return result
    
    async def update(self, id: int, image_in: schemas.ImageIn):
        if not image_in.model_dump(exclude_none=True):
            return True
        
        stmt = (
            update(Image)
            .where(Image.id == id)
            .values(**image_in.model_dump(exclude_none=True))
        )

        await self._session.execute(stmt)
        await self._session.commit()

        return True
    
    async def remove(self, id: int):
        stmt = (
            delete(Image)
            .where(Image.id == id)
        )

        await self._session.execute(stmt)
        await self._session.commit()
