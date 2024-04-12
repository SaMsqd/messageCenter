from flask import Flask, render_template, request, make_response, redirect, url_for
from flask_socketio import SocketIO, send, emit
from functools import wraps


app = Flask(__name__)
socketIO = SocketIO(app, cors_allowed_origins='*', async_mode='threading')


"""
    Декоратор, который проверяет актуальность пароля пользователя, которые хранится в cookie
    В случае его неактуальности, перенаправвляет на страницу login
"""
def check_cookies(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        if request.cookies.get('password') == get_password():
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return decorated_func


def get_password():
    """
    Функция, которая будет получать пароль из файла с ботом и возвращать его
    :return:
    """
    return 'test'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if get_password() == request.cookies.get('password'):
        return redirect(url_for('chats'))

    if request.method == 'POST':
        if request.form.get('password') == get_password():
            print('Обработка прошла успешно')
            res = make_response(redirect(url_for('chats')))
            res.set_cookie('password', request.form.get('password'), max_age=5, expires=5)
            return res

    res = make_response(render_template('index.html'))
    return res


@app.route('/chats')
@check_cookies
def chats():
    return 'Страница с чатами'


@socketIO.on('get_chats')
def get_chats():
    print('Вызвана функция get_chats')
    send(chats())


@socketIO.on('new message')
def new_message():
    print('Вызвана функция new_message')
    send('<НОВОЕ СООБЩЕНИЕ>', broadcast=True)


if __name__ == '__main__':
    socketIO.run(app, host='92.118.114.25', log_output=True, allow_unsafe_werkzeug=True)
