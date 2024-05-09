from fastapi import APIRouter, WebSocket

from app.websocket import WS_Manager


router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")


ws_manager = WS_Manager()

