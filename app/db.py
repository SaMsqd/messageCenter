from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Boolean, Integer, Column, TIMESTAMP, func
from sqlalchemy.future import select

from app.schemas import AccountReceive
from avito.account import AvitoAccountHandler, AccountList

from fastapi import HTTPException

DATABASE_URL = "postgresql+asyncpg://postgresql_vqa7_user:w2rJHucU7Mz5qOFeDC5pDYUIYMYIFShb@dpg-cojan7qcn0vc73drtp6g-a.oregon-postgres.render.com/postgresql_vqa7"


class Base(DeclarativeBase):
    pass


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(
        Integer, unique=True, primary_key=True
    )
    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True, nullable=False
    )
    time_of_registration = Column(TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp())
    hashed_password: Mapped[str] = mapped_column(
        String(length=1024), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )


class avitoAccount(Base):
    __tablename__ = 'avitoAccount'

    account_id = Column(Integer, primary_key=True, unique=True, autoincrement=True)  # В нашем сервисе
    user_id = Column(Integer)  # В нашем сервисе

    profile_id = Column(Integer, unique=True)
    client_id = Column(String, unique=True)
    client_secret = Column(String, unique=True)
    account_name = Column(String)


class avitoChats(Base):
    __tablename__ = 'avitoChats'

    chat_id = Column(String, primary_key=True, unique=True)
    account_id = Column(Integer)
    user_id = Column(Integer)

    color = Column(String, default=None)
    deleted = Column(Boolean, default=False)


class Hints(Base):
    __tablename__ = 'hints'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    account_name = Column(String)

    hint = Column(String)


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


async def accountreceive_to_avitoaccount_db(acc: AccountReceive, user: User) -> avitoAccount:
    return avitoAccount(
        user_id=user.id,
        profile_id=acc.profile_id,
        client_id=acc.client_id,
        client_secret=acc.client_secret,
        account_name=acc.account_name
    )


async def check_account(acc: AccountReceive):
    AvitoAccountHandler(
        profile_id=acc.profile_id,
        client_id=acc.client_id,
        client_secret=acc.client_secret,
        proxy=None,
        name=acc.account_name
    )


async def register_account(acc: AccountReceive, user: User):
    async for session in get_async_session():
        await check_account(acc)
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


async def remember_chat(chat_id, account_name, user_id):
    async for session in get_async_session():
        account = await session.execute(select(avitoAccount).where(avitoAccount.account_name == account_name,
                                                                  avitoAccount.user_id == user_id))
        account_id = account.scalar()
        chat = avitoChats(chat_id=chat_id, account_id=account_id.account_id, user_id=user_id)
        session.add(chat)
        await session.commit()


async def get_all_chats_db(user_id: int):
    async for session in get_async_session():
        res = await session.execute(select(avitoChats).where(avitoChats.user_id == user_id))
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
            return chats
        for account_name, account_data in chats[0].items():
            for chat_data in account_data:
                for chat_id, data in chat_data.items():
                    if chat_id in [db_chat.chat_id for db_chat in db_chats]:
                        data['color'] = [db_chat.color for db_chat in db_chats if db_chat.chat_id == chat_id][0]
                        data['deleted'] = [db_chat.deleted for db_chat in db_chats if db_chat.chat_id == chat_id][0]
                    else:
                        await remember_chat(chat_id, account_name, user_id)       # Сделать функцию добавления чата

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
        if res['hints'] == []:
            raise HTTPException(status_code=404, detail='К этому аккаунту авито не добавлено подсказок')
        return res
