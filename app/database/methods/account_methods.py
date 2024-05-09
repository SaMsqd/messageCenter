from app.database.database_schemas import User, avitoAccount
from app.database.db import get_async_session
from app.schemas import AccountReceive

from avito.account import AvitoAccountHandler

from sqlalchemy.future import select

from fastapi import HTTPException


async def accountreceive_to_avitoaccount_db(acc: AccountReceive, user: User) -> avitoAccount:
    return avitoAccount(
        user_id=user.id,
        profile_id=acc.profile_id,
        client_id=acc.client_id,
        client_secret=acc.client_secret,
        account_name=acc.account_name
    )


async def account_receive_to_handler(acc: AccountReceive) -> AvitoAccountHandler:
    return AvitoAccountHandler(
        profile_id=acc.profile_id,
        client_id=acc.client_id,
        client_secret=acc.client_secret,
        proxy=None,
        name=acc.account_name
    )


async def register_account(acc: AccountReceive, user: User):
    async for session in get_async_session():
        await account_receive_to_handler(acc)
        acc: avitoAccount = await accountreceive_to_avitoaccount_db(acc, user)
        session.add(acc)
        await session.commit()


async def delete_account(acc: AccountReceive, user: User):
    async for session in get_async_session():
        res = await session.execute(select(avitoAccount).where(avitoAccount.profile_id == acc.profile_id,
                                                               avitoAccount.user_id == user.id))
        avito_account = res.scalar()
        if avito_account:
            await session.delete(avito_account)
            await session.commit()
        else:
            raise HTTPException(status_code=404, detail='Аккаунт не найден')


async def get_accounts(user: User):
    async for session in get_async_session():
        res = await session.execute(select(avitoAccount).where(avitoAccount.user_id == user.id))
        avito_accounts = res.scalars()
        res = {}
        if avito_accounts:
            for avito_account in avito_accounts:
                res[avito_account.account_name] = {
                    'profile_id': avito_account.profile_id,
                    'client_id': avito_account.client_id,
                    'client_secret': avito_account.client_secret
                }
        else:
            raise HTTPException(status_code=404, detail='К этому аккаунту не привязан ни один авито')
        return res


async def avitoaccount_db_to_avitoaccounthandler(avito_account: avitoAccount) -> AvitoAccountHandler:
    return AvitoAccountHandler(
        profile_id=avito_account.profile_id,
        client_id=avito_account.client_id,
        client_secret=avito_account.client_secret,
        proxy=None,
        name=avito_account.account_name
    )
