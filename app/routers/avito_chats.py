from fastapi import APIRouter, Depends, Response

from app.database.methods import chat_methods as db
from app.database.db import User
from app.users import current_active_user


router = APIRouter()


@router.get('/get_chats', description="""
    Возвращает список чатов для юзера, за исключением чатов, помеченных как 'удалённые'
""")
async def get_chats(user: User = Depends(current_active_user)):
    return await db.get_all_chats(user.id)


@router.get('/add_hints', description="""Метод для добавления подсказок в чаты(заготовленные фразы)""")
async def add_hints(account_name: str, hint: str, user: User = Depends(current_active_user)):
    await db.add_hints(account_name, hint, user)
    return Response(status_code=201)


@router.get('/get_hints', description="""Метод для получения подсказок для чатов(заготовленные фразы)""")
async def get_hints(account_name: str, user: User = Depends(current_active_user)):
    return await db.get_hints(account_name, user)

