from uuid import UUID

from sqlalchemy import desc, insert, select
from sqlalchemy.orm import joinedload

from src.db.models.hosting import Video
from src.schemas import hosting as schemas

from .base import SQLAlchemyRepo


class VideoRepo(SQLAlchemyRepo):
    async def create(
        self, video_in: schemas.VideoIn, path: str, user_id: UUID
    ) -> schemas.VideoOut:
        stmt = (
            insert(Video)
            .returning(Video)
            .values(
                path=path,
                user_id=user_id,
                **video_in.model_dump(),
            )
        ).options(joinedload(Video.user))

        video = await self._session.scalar(stmt)

        await self._session.commit()
        await self._session.refresh(video)
        return schemas.VideoOut.model_validate(video)

    async def get_by_id(self, id: int) -> schemas.VideoOut:
        query = select(Video).where(Video.id == id).options(joinedload(Video.user))
        video = await self._session.scalar(query)
        # await self._session.refresh(video)

        return schemas.VideoOut.model_validate(video)

    async def get_videos(
        self, limit: int = 5, offset: int = 0
    ) -> list[schemas.VideosOut]:
        query = (
            select(Video)
            .order_by(desc(Video.created_at))
            .limit(limit)
            .offset(offset)
            .options(joinedload(Video.user))
        )
        videos = await self._session.scalars(query)
        print("!!!!!!!", videos)
        # await self._session.refresh(videos)

        return [schemas.VideoOut.model_validate(video) for video in videos]
