import requests
import json


class AvitoApi:
    def __init__(self, profile_id, client_id, client_secret, proxy='83.171.90.83:8080'):
        """
        Сохраняются токен и секрет для генерации запросов к API
        :param int profile_id: ID профиля
        :param str client_id:
        :param str client_secret:
        :param str proxy: Через какой proxy делать запросы
        """
        self.profile_id = profile_id
        self.client_id = client_id
        self.client_secret = client_secret
        if proxy:
            self.proxy = {'https': str(proxy)}
        self.token: str = self.get_token()
        self.headers: dict = {'Authorization': f'Bearer {self.token}'}
        self.chats_queue: list = []
        self.update_chats()

    def get_token(self):
        """
        Получает access_token и возвращает его
        :return:
        """
        data = {
                'grant_type': 'client_credentials',
                'client_id': self.client_id,
                'client_secret': self.client_secret,
        }
        headers = {'Content-Type': 'application/x-www-form-urlencoded',
                   'accept': 'application/json'}
        res = json.loads(
            requests.post('https://api.avito.ru/token/', data=data, headers=headers).content.decode()
        )['access_token']
        return res

    def update_chats(self):
        """
        Возвращает список чатов
        :return list:
        """
        res = json.loads(
            requests.get(
                f'https://api.avito.ru/messenger/v2/accounts/{self.profile_id}/chats',
                    headers=self.headers, params={'limit': 30, 'chat_types': 'u2u,u2i'}).content.decode()
        )
        self.chats_queue = res['chats']

    def get_chat(self, chat_id):
        """
        Получить все сообщения из чата
        :param int chat_id:
        :return:
        """
        headers = self.headers | {'accept': 'application/json'}
        res = json.loads(requests.get(
                f'https://api.avito.ru/messenger/v3/accounts/{self.profile_id}/chats/{chat_id}/messages',
                headers=headers
            ).content.decode())
        return res

    def send_message(self, chat_id, text):
        """
        Отправляет сообщение в чат
        :param int chat_id: id чата, куда нужно отправить сообщение
        :param str text: сообщение для отправки
        :return:
        """
        headers = self.headers | {'accept': 'application/json', 'Content-Type': 'application/json'}
        data = json.dumps({
            'message': {
                'text': text
            },
            'type': 'text'
        })
        response = json.loads(
            requests.post(
                url=f'https://api.avito.ru/messenger/v1/accounts/{self.profile_id}/chats/{chat_id}/messages',
                data=data, headers=headers
            ).content.decode()
        )
        return response['content']['text'] == text

    def register_webhook(self, url: str):
        """Функция, которая будет регистрировать веб-хуки с AvitoAPI"""
        data = json.dumps({
            'url': url
        })
        response = json.load(
            requests.post(url='https://api.avito.ru/messenger/v1/subscriptions',
                          headers=self.headers,
                          data=data)
        )
        if response['ok'] or response['ok'] == 'true':
            print(f'Webhook для аккаунта {self.profile_id} успешно зарегистрирован')
        else:
            print(f'Ошибка регистрации веб-хука для аккаунта {self.profile_id}')
