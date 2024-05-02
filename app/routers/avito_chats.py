from fastapi import APIRouter, Depends

from app.db import User, get_all_chats
from app.users import current_active_user


router = APIRouter()


@router.get('/get_chats', description="""
    Возвращает список чатов для юзера, за исключением чатов, помеченных как 'удалённые'
""")
async def get_chats(user: User = Depends(current_active_user)):
    return await get_all_chats(user.id)
