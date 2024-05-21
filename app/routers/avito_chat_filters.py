from fastapi import APIRouter, Depends

from app.database.db import User
from app.database.methods import filter_methods as db
from app.users import current_active_user

from urllib.parse import unquote

router = APIRouter()


@router.post('/colored', description='Функция для получения чатов определённого цвета')
async def colored(color: str, user: User = Depends(current_active_user)):
    return await db.get_chats_by_color(color, user.id)


@router.post('/accounts', description='Функция для получения чатов определённого аккаунта')
async def accounts(account: str, user: User = Depends(current_active_user)):
    account = unquote(account)
    return await db.get_chats_by_account(account, user.id)
