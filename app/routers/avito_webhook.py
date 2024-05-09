from fastapi import APIRouter

from app.websocket import WS_Manager


router = APIRouter()


ws_manager = WS_Manager()

