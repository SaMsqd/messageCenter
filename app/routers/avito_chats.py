from fastapi import APIRouter, Depends, Response

from app.database.methods import chat_methods as db
from app.database.db import User
from app.schemas import ChatsReceive
from app.users import current_active_user
from avito.account import AvitoAccountHandler
from app.websocket import ws_manager, chat_manager

from app.routers.avito_chat_filters import router as avito_chat_filters

from urllib.parse import unquote

import time


router = APIRouter()

router.include_router(avito_chat_filters, prefix='/filters', tags=['filters'])


@router.get('/get_chats', description="""
    Возвращает список чатов для юзера, за исключением чатов, помеченных как 'удалённые'
""")
async def get_chats(user: User = Depends(current_active_user)):
    return await db.get_all_chats(user.id)


@router.get('/add_hints', description="""Метод для добавления подсказок в чаты(заготовленные фразы)""")
async def add_hints(account_name: str, hint: str, user: User = Depends(current_active_user)):
    account_name = unquote(account_name)
    await db.add_hints(account_name, hint, user)
    return Response(status_code=201)


@router.get('/get_hints', description="""Метод для получения подсказок для чатов(заготовленные фразы)""")
async def get_hints(account_name: str, user: User = Depends(current_active_user)):
    account_name = unquote(account_name)
    return await db.get_hints(account_name, user)


@router.post('/set_colors', description='Метод для изменения цвета чата')
async def set_colors(chats_id: ChatsReceive, color: str, user: User = Depends(current_active_user)):
    return await db.set_colors(chats_id.model_dump()['chats'], color, user)


@router.post('/delete_chats', description='Пометить чат как удалённый')
async def delete_chats(chats_id: ChatsReceive, user: User = Depends(current_active_user)):
    return await db.delete_chats(chats_id.dict.model_dump()['chats'], user)


@router.post('/get_chat', description='Получить список всех сообщений в чате')
async def get_chat(chat_id: str, account_name: str, user: User = Depends(current_active_user)):
    account_name = unquote(account_name)
    return await db.get_chat(chat_id, account_name, user)


@router.post('/send_message', description='Отправить сообщение в чат')
async def send_message(chat_id: str, account_name: str, message: str, user: User = Depends(current_active_user)):
    account_name = unquote(account_name)
    account: AvitoAccountHandler = await db.get_account(account_name, user)
    return account.api.send_message(chat_id, message)
