from app.database.db import get_async_session
from app.database.database_schemas import avitoAccount, avitoChats
from sqlalchemy.future import select

from fastapi import HTTPException

from avito.account import AvitoAccountHandler, AccountList


async def get_chats_by_color(color: str, user_id: int):
    async for session in get_async_session():
        res = await session.execute(select(avitoChats).where(avitoChats.color == color,
                                                             avitoChats.user_id == user_id))
        chats = res.scalars()
        if chats:
            return chats
        else:
            raise HTTPException(status_code=404, detail='Чаты не найдены')


async def account_avito_to_handler(acc: avitoAccount) -> AvitoAccountHandler:
    return AvitoAccountHandler(
        profile_id=acc.profile_id,
        client_id=acc.client_id,
        client_secret=acc.client_secret,
        proxy=None,
        name=acc.account_name
    )


async def get_chats_by_account(account_name: str, user_id: int):
    async for session in get_async_session():
        account_res = await session.execute(select(avitoAccount).where(avitoAccount.account_name == account_name,
                                                                       avitoAccount.user_id == user_id))
        account_list: AccountList = AccountList()
        account: avitoAccount = account_res.scalars().first()

        if not account:
            raise HTTPException(status_code=404, detail='Аккаунт не найден')

        account: AvitoAccountHandler = await account_avito_to_handler(account)
        account_list.add(account)
        chats = account_list.get_chats()

        if chats:
            return chats
        else:
            raise HTTPException(status_code=404, detail='Чаты не найдены')
