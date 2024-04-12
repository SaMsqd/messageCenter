import avito_api


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
