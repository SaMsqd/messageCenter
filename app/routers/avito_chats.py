from fastapi import APIRouter, Depends, Response

from app.database.methods import chat_methods as db
from app.database.db import User
from app.users import current_active_user
from avito.account import AvitoAccountHandler


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


@router.post('/set_color', description='Метод для изменения цвета чата')
async def set_color(chat_id: str, color: str, user: User = Depends(current_active_user)):
    return await db.set_color(chat_id, color, user)


@router.post('/delete_chat', description='Пометить чат как удалённый')
async def delete_chat(chat_id: str, user: User = Depends(current_active_user)):
    return await db.delete_chat(chat_id, user)


@router.post('/get_chat', description='Получить список всех сообщений в чате')
async def get_chat(chat_id: str, account_name: str, user: User = Depends(current_active_user)):
    return await db.get_chat(chat_id, account_name, user)


@router.post('/send_message', description='Отправить сообщение в чат')
async def send_message(chat_id: str, account_name: str, message: str, user: User = Depends(current_active_user)):
    account: AvitoAccountHandler = await db.get_account(account_name, user)
    return account.api.send_message(chat_id, message)
