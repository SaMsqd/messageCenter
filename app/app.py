import asyncio

import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

from app.database.db import create_db_and_tables, recreate_db_and_tables
from app.schemas import UserCreate, UserRead, UserUpdate
from app.users import auth_backend, fastapi_users
from app.routers import avito_chats, avito_accounts, avito_webhook

import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Not needed if you setup a migration system like Alembic
    await create_db_and_tables()
    yield




app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Здесь можно указать разрешенные источники (origins)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

app.include_router(
    avito_accounts.router,
    prefix='/avito_accounts',
    tags=['avito_accounts']
)

app.include_router(
    avito_chats.router,
    prefix='/avito_chats',
    tags=['avito_chats']
)

app.include_router(
    avito_webhook.router,
    prefix='/avito_webhook',
    tags=['avito_webhook']
)


@app.websocket('/endless_ws')
async def endless_ws(ws: WebSocket):
    await ws.accept()
    for i in range(9999):
        await ws.send_text(str(i))
        time.sleep(5)


uvicorn.run(app, host='0.0.0.0', port=10000)
