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
            {
                'grant_type': 'client_credentials',
                'client_id': self.client_id,
                'client_secret': self.client_secret,
            }
        }
        return json.loads(
            requests.get('https://api.avito.ru/token/', data=data, proxies=self.proxy).content.decode()
        )['access_token']

    def update_chats(self):
        """
        Возвращает список чатов
        :return list:
        """
        res = json.loads(
            requests.get(
                f'https://api.avito.ru/messenger/v2/accounts/{self.profile_id}/chats',
                proxies=self.proxy, headers=self.headers)
        )
        self.chats_queue = res.content['chats']

    def get_chat(self, chat_id):
        """
        Получить все сообщения из чата
        :param int chat_id:
        :return:
        """
        res = json.loads(
            requests.get(
                f'https://api.avito.ru/messenger/v2/accounts/{self.profile_id}/chats/{chat_id}/messages',
                proxies=self.proxy, headers=self.headers
            )
        )
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
                data=data, headers=headers, proxies=self.proxy
            )
        )
        return response['content']['text'] == text
