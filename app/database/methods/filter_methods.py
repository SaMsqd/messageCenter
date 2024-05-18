from app.database.db import get_async_session
from app.database.database_schemas import avitoAccount, avitoChats
from sqlalchemy.future import select

from fastapi import HTTPException


async def get_chats_by_color(color: str, user_id: int):
    async for session in get_async_session():
        res = await session.execute(select(avitoChats).where(avitoChats.color == color,
                                                             avitoChats.user_id == user_id))
        chats = res.scalars()
        if chats:
            return chats
        else:
            raise HTTPException(status_code=404, detail='Чаты не найдены')


async def get_chats_by_account(account_id: str, user_id: int):
    async for session in get_async_session():
        res = await session.execute(select(avitoChats).where(avitoChats.account_id == account_id,
                                                             avitoChats.user_id == user_id))
        chats = res.scalars()
        if chats:
            return chats
        else:
            raise HTTPException(status_code=404, detail='Чаты не найдены')
