from fastapi import APIRouter, WebSocket, Request

from app.websocket import ws_manager, chat_manager


router = APIRouter()


@router.post('/{user_id}/accept')
async def webhook_accept(user_id: int, request: Request):
    data = await request.json()
    await ws_manager.broadcast(user_id, data, 'in')
    await chat_manager.broadcast(data, direction_in=True)


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)


@router.websocket("/chats")
async def chat_endpoint(websocket: WebSocket):
    await chat_manager.connect(websocket)
