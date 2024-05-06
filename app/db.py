from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Boolean, Integer, Column
from sqlalchemy.future import select

from app.schemas import AccountReceive
from avito.account import AvitoAccountHandler, AccountList

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


engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
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


async def delete_account(acc: AccountReceive, user):
    async for session in get_async_session():
        res = await session.execute(select(avitoAccount).where(avitoAccount.profile_id == acc.profile_id,
                                                               avitoAccount.user_id == user.id))
        avito_account = res.scalar()
        if avito_account:
            await session.delete(avito_account)
            await session.commit()
        else:
            return {'status_code': 404, 'detail': 'Аккаунт не найден'}


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
