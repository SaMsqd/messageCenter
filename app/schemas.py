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
