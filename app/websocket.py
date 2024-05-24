import json
import time
from functools import singledispatch

from fastapi import WebSocket
from starlette.websockets import WebSocketDisconnect

from app.database.methods import user_methods as db


class WSManager:
    def __init__(self):
        self.connections = {}   # Тут будут храниться все подключенные клиенты в виде {user_id: [socket]}

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        email = await websocket.receive_text()
        user = await db.get_user(email)
        if not user:
            await websocket.send_text('Пользователь не найден, подключение не защитано')
            return
        user_id = user.id
        if self.connections.get(user_id, None):
            self.connections[user_id].append(websocket)
        else:
            self.connections[user_id] = [websocket]
        await websocket.send_text(f'Веб-сокет успешно зарегистрирован!{user_id}')

    async def broadcast(self, user_id: int, data: dict):
        try:
            for socket in self.connections[user_id]:
                try:
                    await socket.send_text(json.dumps(data))
                except RuntimeError and WebSocketDisconnect:
                    self.connections[user_id].remove(socket)
        except KeyError:
            pass


class ChatManager(WSManager):
    async def broadcast(self, data: dict, **kwargs):
        chat_id = data['payload']['value']['chat_id']
        try:
            for socket in self.connections[chat_id]:
                try:
                    await socket.send_text(json.dumps(data))
                except RuntimeError and WebSocketDisconnect:
                    self.connections[chat_id].remove(socket)
        except KeyError:
            pass

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        chat_id = await websocket.receive_text()
        if self.connections.get(chat_id, None):
            self.connections[chat_id].append(websocket)
        else:
            self.connections[chat_id] = [websocket]
        await websocket.send_text(f'Веб-сокет успешно зарегистрирован!{chat_id}')


ws_manager = WSManager()
chat_manager = ChatManager()
