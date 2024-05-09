from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from .database_schemas import User, Base

DATABASE_URL = "postgresql+asyncpg://postgresql_vqa7_user:w2rJHucU7Mz5qOFeDC5pDYUIYMYIFShb@dpg-cojan7qcn0vc73drtp6g-a.oregon-postgres.render.com/postgresql_vqa7"


engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def recreate_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
