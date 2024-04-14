from avito import avito_api


class ProxyException(BaseException):
    def __init__(self, message=''):
        super().__init__()
        self.message = message


class Account:
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

    def add(self, account: Account):
        self.accounts.append(account)

    def send_message(self, account_name, chat_id, message):
        for account in self.accounts:
            if account.name == account_name:
                account.api.send_message(chat_id=chat_id, text=message)

    def get_chats(self):
        res = []
        for account in self.accounts:
            chats = []
            for chat in account.api.chats_queue:
                chats.append({chat['id']: chat['context']['value']['title']})
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
