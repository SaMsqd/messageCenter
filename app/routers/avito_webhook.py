from fastapi import APIRouter, WebSocket

from app.websocket import WSManager
from app.schemas import WebHookReceive


router = APIRouter()


@router.post('/{user_id}/accept')
def webhook_accept(user_id: int, data: WebHookReceive):
    ws_manager.broadcast(user_id, data.model_dump())


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)


ws_manager = WSManager()

