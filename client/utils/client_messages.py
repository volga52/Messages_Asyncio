from datetime import datetime


class JimClientMessage:
    def auth(self, username, password):
        """
        Authorization message
        :param username: имя пользователя
        :param password: пароль
        :return: dict with data
        """
        data = {
            'action': 'authenticate',
            'time': datetime.now().timestamp(),
            # 'type': 'auth',
            'user': {
                'account_name': username,
                'password': password
            }
        }
        return data

    def presence(self, sender, status="Yep, I am here!"):
        """
        Presence messages, which notify server that client is online
        :param sender: username
        :param status: some text
        :return: dict with data
        """
        data = {
            "action": "presence",
            "time": datetime.now().timestamp(),
            "type": "status",
            "user": {
                "account_name": sender,
                "status": status
            }
        }
        return data

    def quit(self, sender, status='disconnect'):
        """
        Сообщение пользователя о выходе
        :param sender: username
        :param status: тип сообщения
        :return: словарь с данными о выходе
        """
        data = {
            'action': 'quit',
            'time': datetime.now().timestamp(),
            'type': 'status',
            'user': {
                'account_name': sender,
                'status': status
            }
        }
        return data

    def list_(self, sender, status='show', person=''):
        """
        Сообщение запрос на весь список контактов
        :param sender: user_name
        :param status: тип запроса
        :param person: имя
        :return: словарь с данными
        """
        data = {
            'action': 'list',
            'time': datetime.now().timestamp(),
            'type': 'status',
            'contact_list': 'No contact yet',
            'user': {
                'account_name': sender,
                'status': status,
                'contacts': person
            }
        }
        return data

    def message(self, sender, receiver='user1', text='some messages text'):
        """
        Пересылаемое сообщение
        :param sender: получатель
        :param receiver: отправитель
        :param text: текст сообщения
        :return: словарь с данными сообщения
        """
        data = {
            'action': 'message',
            'time': datetime.now().timestamp(),
            'to': receiver,
            'from': sender,
            'encoding': 'utf-8',
            'message': text
        }
        return data
