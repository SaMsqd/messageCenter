from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Boolean, Integer, Column, TIMESTAMP, func

from fastapi_users.db import SQLAlchemyBaseUserTable


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

    client_name: Mapped[str] = mapped_column(
        String(length=320), default=None
    )


class Hints(Base):
    __tablename__ = 'hints'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    account_name = Column(String)

    hint = Column(String)
