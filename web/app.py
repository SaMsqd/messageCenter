import os
import time

import fastapi
from fastapi import WebSocket, Depends
from fastapi.responses import HTMLResponse, Response

from avito.account import Account, AccountList

from auth.users import fastapi_users, auth_backend, User, current_active_user
from auth.schemas import UserRead, UserCreate, UserUpdate

import uvicorn


app = fastapi.FastAPI()
accounts = AccountList()

accounts.add(Account(profile_id=159470220,
                     client_id='Pm4BmvaY4LPFHQ6Oo_Hu',
                     client_secret='qBO1H1ssvcfotR15Nw1Qpxrs_1yG9vyhWb9tbgj5',
                     proxy=None,
                     name='first'))


class Manager:
    def __init__(self):
        self.active_connections = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active_connections.append(ws)

    async def disconnect(self, ws: WebSocket):
        print('Юзер ')
        self.active_connections.remove(ws)

    async def send_message(self, ws: WebSocket, message):
        await ws.send_text(message)

    async def broadcast(self, message):
        for con in self.active_connections:
            try:
                await con.send_text(message)
            except Exception:
                pass


manager = Manager()


def return_html(file_name, headers: dict = None):
    with open(f'./web/templates/{file_name}') as f:
        return f.read()


@app.websocket('/connect_ws')
async def web_socket(ws: WebSocket):
    await manager.connect(ws)


@app.websocket('/endless_ws')
async def endless_ws(ws: WebSocket):
    await ws.accept()
    while True:
        print("Отправленно сообщение")
        await ws.send_text('Some data From WS 2')
        time.sleep(5)
  

    # await ws.close()

@app.get('/chats', response_class=fastapi.responses.HTMLResponse, tags=['html'])
@app.post('/chats', response_class=fastapi.responses.HTMLResponse, tags=['html'])
#@check_cookies
async def chats():
    return return_html('chats.html')


@app.post('/get_messages', tags=['avito_api'])
async def api_get_messages(account_name, chat_id):
    return accounts.get_messages(account_name, chat_id)


@app.post('/send_message', tags=['avito_api'])
async def api_send_message(account_name, chat_id, message):
    accounts.send_message(account_name, chat_id, message)
    return 200


@app.get('/get_chats', tags=['avito_api'])
async def api_get_chats():
    return accounts.get_chats()


@app.get('/send_messages', tags=['web_socket'])
async def ws_send_messages():
    try:
        await manager.broadcast('Test')
    except Exception:
        pass


app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix='/auth', tags=['auth'],
)


app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate), prefix='/auth', tags=['register'],
)

app.include_router(
    fastapi_users.get_reset_password_router(), prefix='/auth', tags=['auth']
)

app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/users",
    tags=["users"],
)

app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)


@app.get("/authenticated-route", tags=['test_auth'])
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}

uvicorn.run(app, host=os.getenv('HOST'), port=int(os.getenv('PORT')))
