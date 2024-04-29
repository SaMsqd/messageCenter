from pydantic import BaseModel


class AccountSchema(BaseModel):
    profile_id: int
    client_id: str
    client_secret: str
    account_name: str
