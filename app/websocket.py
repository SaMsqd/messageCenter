import json

from fastapi import WebSocket
from app.database.methods import user_methods as db


class WSManager:
    def __init__(self):
        self.connections = {}   # Тут будут хранится все подключенные клиенты в виде {user_id: [socket]}

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        email = await websocket.receive_text()

        user = await db.get_user(email)
        user_id = user.id
        if self.connections.get(user_id, None):
            self.connections[user_id].append(websocket)
        else:
            self.connections[user_id] = [websocket]
        await websocket.send_text('Веб-сокет успешно зарегистрирован!')

    async def broadcast(self, user_id: int, data: dict):
        for socket in self.connections[user_id]:
            try:
                await socket.send_json(json.dumps(data))
            except RuntimeError:
                await socket.close()

