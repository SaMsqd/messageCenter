from fastapi import APIRouter, WebSocket, Request

from app.websocket import ws_manager


router = APIRouter()


@router.post('/{user_id}/accept')
async def webhook_accept(user_id: int, request: Request):
    data = await request.json()
    print(data)
    await ws_manager.broadcast(user_id, data)


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
