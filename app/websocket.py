from fastapi import WebSocket


class WS_Manager:
    def __init__(self):
        self.connections = {}   # Тут будут хранится все подключенные клиенты в виде {user_id: socket}

    def connect(self, websocket: WebSocket, user_id: int):
        self.connections[user_id] = websocket

    def disconnect(self, user_id: int):
        self.connections.pop(user_id)

    def broadcast(self, user_id: int, data: dict):
        for socket in self.connections[user_id]:
            socket.send_json(data)
