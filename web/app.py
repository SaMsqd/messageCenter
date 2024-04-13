import fastapi
from fastapi import WebSocket
import uvicorn


app = fastapi.FastAPI()


class Manager:
    def __init__(self):
        self.active_connections = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active_connections.append(ws)

    async def disconnect(self, ws: WebSocket):
        self.active_connections.remove(ws)

    async def send_message(self, ws: WebSocket, message):
        await ws.send_text(message)

    async def broadcast(self, message):
        for con in self.active_connections:
            await con.send_text(message)

# def check_cookies(f):
#     """
#         Декоратор, который проверяет актуальность пароля пользователя, которые хранится в cookie
#         В случае его неактуальности, перенаправвляет на страницу login
#     """
#     @wraps(f)
#     def decorated_func(*args, **kwargs):
#         if request.cookies.get('password') == get_password():
#             return f(*args, **kwargs)
#         else:
#             return redirect(url_for('login'))
#     return decorated_func


manager = Manager()


def return_html(file_name):
    with open(f'./templates/{file_name}') as f:
        return f.read()


async def get_password():
    """
    Функция, которая будет получать пароль из файла с ботом и возвращать его
    :return:
    """
    return 'test'


@app.get('/login', response_class=fastapi.responses.HTMLResponse)
@app.post('/login', response_class=fastapi.responses.HTMLResponse)
async def login():
    return return_html('index.html')

@app.websocket('/')
async def web_socket(ws: WebSocket):
    await manager.connect(ws)
    while True:
        data = await ws.receive_text()
        await manager.broadcast(data)

@app.get('/chats', response_class=fastapi.responses.HTMLResponse)
@app.post('/chats', response_class=fastapi.responses.HTMLResponse)
#@check_cookies
def chats():
    return return_html('chats.html')


uvicorn.run(app, port=5000, host='127.0.0.1')
