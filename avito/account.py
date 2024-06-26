from avito import avito_api
from datetime import datetime


class ProxyException(BaseException):
    def __init__(self, message=''):
        super().__init__()
        self.message = message


class AvitoAccountHandler:
    """
    Класс, через который будет осуществляться работа с api + взаимодействие с сервером
    """

    def __init__(self, profile_id, client_id, client_secret, proxy, name):
        self._api = avito_api.AvitoApi(profile_id, client_id, client_secret, proxy)
        self.name = name

    @property
    def api(self):
        try:
            self.check_proxy()
            return self._api
        except ProxyException as ex:
            print(f'Произошла ошибка с прокси у аккауна {self.name}, операция с api не выполнена')

    def check_proxy(self):
        pass


class AccountList:
    def __init__(self):
        self.accounts = list()

    def add(self, account: AvitoAccountHandler):
        self.accounts.append(account)

    def send_message(self, account_name, chat_id, message):
        for account in self.accounts:
            if account.name == account_name:
                account.api.send_message(chat_id=chat_id, text=message)

    @staticmethod
    def get_account_name(chats):
        names = []
        for chat in chats:
            if len(names) == 0:
                names.append(chat['users'][0]['name'])
                names.append(chat['users'][1]['name'])
            else:
                if chat['users'][0]['name'] in names:
                    return chat['users'][0]['name']
                else:
                    return chat['users'][1]['name']

    @staticmethod
    def get_client_name(chat, account_name):
        if chat['users'][0]['name'] == account_name:
            return chat['users'][1]['name']
        else:
            return chat['users'][0]['name']

    def get_chats(self):
        res = []
        for account in self.accounts:
            chats = []
            avito_account_name = AccountList.get_account_name(account.api.chats_queue)
            for chat in account.api.chats_queue:
                last_message = account.api.get_last_message(chat['id'])
                time = int(last_message['messages'][0]['created'])
                time = datetime.utcfromtimestamp(time).strftime('%d-%m-%Y')
                last_message['messages'][0]['created'] = time
                chats.append(
                    {chat['id']: {
                        'title': chat['context']['value']['title'],
                        'last_message': last_message['messages'][0],
                        'client_name': AccountList.get_client_name(chat, avito_account_name),
                    }
                })
            res.append({account.name: chats})
        return res

    def get_messages(self, account_name, chat_id):
        res = []
        for account in self.accounts:
            if account.name == account_name:
                for message in account.api.get_chat(chat_id)['messages'][::-1]:
                    res.append({
                        'content': message['content']['text'],
                        'created': message['created'],
                        'direction': message['direction'],
                        'is_read': message['isRead']
                    })
        return res
