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
        print(email)
        user = await db.get_user(email)
        user_id = user.id
        if self.connections.get(user_id, None):
            self.connections[user_id].append(websocket)
        else:
            self.connections[user_id] = [websocket]
        await websocket.send_text(f'Веб-сокет успешно зарегистрирован!{user_id}')
        print('Веб-сокет зарегестрирован')

    async def broadcast(self, user_id: int, data: dict, direction: str = 'in'):
        try:
            for socket in self.connections[user_id]:
                try:
                    data['payload']['direction'] = direction
                    await socket.send_text(json.dumps(data))
                except RuntimeError and WebSocketDisconnect:
                    self.connections[user_id].remove(socket)
        except KeyError:
            pass


class ChatManager(WSManager):

    @singledispatch
    async def broadcast(self, data: dict, direction: str = 'in', **kwargs):
        chat_id = data['payload']['value']['chat_id']
        try:
            for socket in self.connections[chat_id]:
                try:
                    data['payload']['direction'] = direction
                    await socket.send_text(json.dumps(data))
                except RuntimeError and WebSocketDisconnect:
                    self.connections[chat_id].remove(socket)
        except KeyError:
            pass

    @broadcast.register
    async def _(self, data: dict, direction_out: bool):
        chat_id = data['payload']['value']['chat_id']
        data['created'] = str(time.time())[:str(time.time()).find('.') + 3]
        try:
            for socket in self.connections[chat_id]:
                try:
                    await socket.send_text(json.dumps(data))
                except RuntimeError and WebSocketDisconnect:
                    self.connections[chat_id].remove(socket)
        except KeyError:
            pass

    @broadcast.register
    async def _(self, data: dict, direction_in: bool):
        chat_id = data['payload']['value']['chat_id']
        res = dict()
        res['created'] = str(time.time())[:str(time.time()).find('.') + 3]
        res['payload'] = dict()
        res['text'] = data['payload']['value']['content']['text']
        res['payload']['value']['chat_id'] = chat_id
        res['direction'] = 'in'
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
