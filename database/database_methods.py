import asyncio

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from database.main import AvitoAccounts, User

from avito.account import Account

from auth.users import current_active_user

from fastapi import Depends


async def account_to_avitoaccount_db(acc: Account, user: User):
    return AvitoAccounts(
        user_id=user.id,
        profile_id=acc.api.profile_id,
        client_id=acc.api.client_id,
        client_secret=acc.api.client_secret,
        account_name=acc.api.account_name
    )


async def register_account(acc: Account, async_session: async_sessionmaker[AsyncSession], user: User):
    async with async_session() as session:
        acc = await account_to_avitoaccount_db(acc, user)
        session.add(acc)
        await session.commit()


if __name__ == '__main__':
    from database.main import session as sess

    account = Account(profile_id=159470220,
                     client_id='Pm4BmvaY4LPFHQ6Oo_Hu',
                     client_secret='qBO1H1ssvcfotR15Nw1Qpxrs_1yG9vyhWb9tbgj5',
                     proxy=None,
                     name='first')
    asyncio.run(register_account(account, sess))
