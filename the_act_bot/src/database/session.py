import os

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from the_act_bot.src.core.config import settings


engine = create_async_engine(settings.database_url, echo=True)
session_maker = async_sessionmaker(autoflush=False, expire_on_commit=False, bind=engine)


async def get_session():
    async with session_maker() as session:
        yield session
