from app.database.database_schemas import User, avitoAccount, avitoChats, Hints
from app.database.db import get_async_session
from app.database.methods.account_methods import get_account

from sqlalchemy.future import select

from fastapi import HTTPException

from app.database.methods.account_methods import avitoaccount_db_to_avitoaccounthandler
from avito.account import AccountList, AvitoAccountHandler


async def remember_chat(client_name: str, chat_id: str, account_name: str, user_id: int ):
    async for session in get_async_session():
        account = await session.execute(select(avitoAccount).where(avitoAccount.account_name == account_name,
                                                                  avitoAccount.user_id == user_id))
        account_id = account.scalar()
        chat = avitoChats(client_name=client_name, chat_id=chat_id, account_id=account_id.account_id, user_id=user_id)
        session.add(chat)
        await session.commit()


async def get_all_chats_db(user_id: int):
    async for session in get_async_session():
        res = await session.execute(select(avitoChats).where(avitoChats.user_id == user_id))
        return res.scalars().all()


async def get_account_chats_db(account_id: int):
    async for session in get_async_session():
        res = await session.execute(select(avitoChats).where(avitoChats.account_id == account_id))
        return res.scalars().all()


async def get_all_chats(user_id):
    async for session in get_async_session():
        res = await session.execute(select(avitoAccount).where(avitoAccount.user_id == user_id))
        account_list = AccountList()
        for acc in res.scalars().all():
            account_list.add(await avitoaccount_db_to_avitoaccounthandler(acc))

        chats = account_list.get_chats()
        db_chats = await get_all_chats_db(user_id)
        if len(chats) == 0:
            raise HTTPException(status_code=404, detail='Не удалось получить чаты')
        for account_name, account_data in chats[0].items():
            for chat_data in account_data:
                for chat_id, data in chat_data.items():
                    if chat_id in [db_chat.chat_id for db_chat in db_chats]:
                        data['color'] = [db_chat.color for db_chat in db_chats if db_chat.chat_id == chat_id][0]
                        data['deleted'] = [db_chat.deleted for db_chat in db_chats if db_chat.chat_id == chat_id][0]
                        data['client_name'] = [db_chat.client_name for db_chat in db_chats if db_chat.chat_id == chat_id][0]
                    else:
                        await remember_chat(data['client_name'], chat_id, account_name, user_id)

        return chats


async def get_account_messages(account_name: str, user_id: int):
    async for session in get_async_session():
        res = await session.execute(select(avitoAccount).where(avitoAccount.account_name == account_name,
                                                              avitoAccount.user_id == user_id))
        account = res.scalar()
        account_list = AccountList()
        if account:
            account_list.add(await avitoaccount_db_to_avitoaccounthandler(account))
        else:
            raise HTTPException(status_code=404, detail='Аккаунт не найден')

        chats = account_list.get_chats()
        db_chats = await get_account_chats_db(user_id)

        if len(chats) == 0:
            raise HTTPException(status_code=404, detail='Сообщения не найдены')

        for account_name, account_data in chats[0].items():
            for chat_data in account_data:
                for chat_id, data in chat_data.items():
                    if chat_id in [db_chat.chat_id for db_chat in db_chats]:
                        data['color'] = [db_chat.color for db_chat in db_chats if db_chat.chat_id == chat_id][0]
                        data['deleted'] = [db_chat.deleted for db_chat in db_chats if db_chat.chat_id == chat_id][0]
                        data['client_name'] = [db_chat.client_name for db_chat in db_chats if db_chat.chat_id == chat_id][0]
                    else:
                        await remember_chat(data['client_name'], chat_id, account_name, user_id)

        return chats


async def check_hint_unique(hint: str, account_name: str, user_id: int):
    async for session in get_async_session():
        res = await session.execute(select(Hints).where(Hints.hint == hint,
                                                        Hints.account_name == account_name,
                                                        Hints.user_id == user_id))
        if res.scalar() is not None:
            raise HTTPException(status_code=409, detail='Такая подсказка уже есть')


async def add_hints(account_name: str, hint: str, user: User):
    async for session in get_async_session():
        res = await session.execute(select(avitoAccount).where(avitoAccount.account_name == account_name,
                                                              avitoAccount.user_id == user.id))
        account = res.scalar()
        if account:
            await check_hint_unique(hint, account_name, user.id)
            hints = Hints(account_name=account.account_name, hint=hint, user_id=user.id)
            session.add(hints)
            await session.commit()
        else:
            raise HTTPException(status_code=404, detail='Аккаунт не найден')


async def get_hints(account_name: str, user: User):
    async for session in get_async_session():
        res = await session.execute(select(Hints).where(Hints.account_name == account_name,
                                                        Hints.user_id == user.id))
        hints = res.scalars()
        res = {'hints': []}
        for hint in hints:
            res['hints'].append(hint.hint)
        if not res['hints']:
            raise HTTPException(status_code=404, detail='К этому аккаунту авито не добавлено подсказок')
        return res


async def set_colors(chats_id: list, color: str, user: User):
    exceptions = []
    async for session in get_async_session():
        for chat_id in chats_id:
            res = await session.execute(select(avitoChats).where(avitoChats.chat_id == chat_id,
                                                                  avitoChats.user_id == user.id))
            chat = res.scalar()
            if chat:
                chat.color = color
                await session.commit()
            else:
                exceptions.append(chat_id)
    if exceptions:
        raise HTTPException(status_code=404, detail=f'Чат(ы) не найдены: {exceptions}')


async def get_chat(chat_id: str, account_name, user: User):
    account: AvitoAccountHandler = await get_account(account_name, user)
    return account.api.get_chat(chat_id)


async def delete_chats(chats_id: list, user: User):
    exceptions = []
    async for session in get_async_session():
        for chat_id in chats_id:
            res = await session.execute(select(avitoChats).where(avitoChats.chat_id == chat_id,
                                                                  avitoChats.user_id == user.id))
            chat = res.scalar()
            if chat:
                chat.deleted = True
                await session.commit()
            else:
                exceptions.append(chat_id)
    if exceptions:
        raise HTTPException(status_code=404, detail=f'Чат(ы) не найдены: {exceptions}')
