class AvitoApi:
    def __init__(self, token, secret):
        """
        Сохраняются токен и секрет для генерации запросов к API
        :param str token:
        :param str secret:
        """

        # Очередь чатов. Обновляется в методе update_unreaden_chats
        self.token = token
        self.secret = secret
        self.chats_queue = None
        self.update_unreaden_chats()

    def update_unreaden_chats(self):
        """
        Добавляет непрочитанные чаты
        :return:
        """
        pass

    def send_message(self, chat):
        """
        Отправляет сообщение в чат
        :param Chat chat: аргумент - объект класса Chat
        :return:
        """
        pass


class Chat:
    def __init__(self):
        """
        Сразу создаётся список сообщений с двумя вложенными словарями. По первому индексу идёт тот,
        кто прислал первое сообщение. По последнему индексу идёт тот, кто прислал последнее сообщение
        {'seller': 'messages_text'} {'buyer': 'messages_text'}
        :return:
        """
        self.messages_queue = None

    def get_last_messages(self):
        """
        Получает последние сообщения, отправленные пользователем и продавцом(может быть очередь сообщений,
        но подряд говорят по разу). Как начнёшь это делать - напиши мне, объясню на примере, не знаю как
        текстом это сделать
        :return: list список с двумя вложенными словарями. По индексу 1(последнему) идёт тот, кто прислал
        последнее сообщение
        {'seller': 'messages_text'}, {'buyer': 'messages_text'}
        """
        pass

    def send_message(self, text):
        """
        Отправляет сообщение в этот чат
        :param str text: Сообщение, которое нужно отправить
        :return:
        """
        pass
