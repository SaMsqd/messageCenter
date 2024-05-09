from fastapi import APIRouter, WebSocket, Depends
from fastapi.responses import Response

from app.schemas import WebHookReceive
from app.database.db import User
from app.users import current_active_user
from app.websocket import WS_Manager


router = APIRouter()


ws_manager = WS_Manager()


@router.post('/webhook/{user_id}/accept')
async def web_hook_accept(user_id: int, web_hook_data: WebHookReceive):
    ws_manager.broadcast(user_id, web_hook_data.dict())


@router.websocket('/websocket/')
async def connect_websocket(ws: WebSocket):
    await ws.accept()
    ws_manager.connect(ws)


@router.websocket('/socket.io/')
async def connect_websocket(ws: WebSocket):
    await ws.accept()
    ws_manager.connect(ws)


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")
