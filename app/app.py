import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.db import create_db_and_tables, recreate_db_and_tables
from app.schemas import UserCreate, UserRead, UserUpdate
from app.users import auth_backend, fastapi_users
from app.routers import avito_chats, avito_accounts, avito_webhook


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield


app = FastAPI(redoc_url=None,
              openapi_url='/openapi.json',
              docs_url='/docs',
              root_path='/api',
              title='Message Center API',
              )


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
