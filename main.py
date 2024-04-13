import asyncio
from web import app, Websocket
import threading


def start_server():
    asyncio.run(app.main())


def open_ws():
    asyncio.run(websocket.main())

def main():
    thread_server = threading.Thread(target=start_server)
    thread_ws = threading.Thread(target=open_ws)

    thread_server.start()
    thread_ws.start()


if __name__ == '__main__':
    main()
