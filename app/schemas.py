from typing import Any

from pydantic import BaseModel
from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    pass


class UserCreate(schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass


class AccountReceive(BaseModel):
    profile_id: int
    client_id: str
    client_secret: str
    account_name: str


class WebHookReceive(BaseModel):
    author_id: int
    chat_id: str
    chat_type: str
    content: Any
    created: int
    id: str
    item_id: str
    read: int
    type: str
    user_id: int
