from app.database.database_schemas import User
from app.database.db import get_async_session

from sqlalchemy.future import select


async def get_user(email: str) -> User:
    async for session in get_async_session():
        res = await session.execute(select(User).where(User.email == email))
        user = res.scalar()
        return user
