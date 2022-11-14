from json import dumps, loads

from server.database.db_controller import ClientMessages
from server.database.models import Base
from server.server_config import ENCODING


class DbInterfaceMixin:
    def __init__(self, db_path):
        # init DB
        self._cm = ClientMessages(db_path, Base, echo=False)

    def add_client(self, username, info=None):
        return self._cm.add_client(username, info)

    def get_client_by_username(self, username):
        return self._cm.get_client_by_username(username)

    def add_client_history(self, client_username, ip_address='8.8.8.8'):
        return self._cm.add_client_history(client_username, ip_address)

    def set_user_online(self, client_username):
        return self._cm.set_user_online(client_username)

    def add_contact(self, client_username, contact_username):
        return self._cm.add_contact(client_username, contact_username)

    def del_contact(self, client_username, contact_username):
        return self._cm.del_contact(client_username, contact_username)

    def get_contacts(self, client_username):
        return self._cm.get_contacts(client_username)

    def get_all_clients(self):
        return self._cm.get_all_clients()

    def get_client_history(self, client_username):
        return self._cm.get_client_history(client_username)

    def get_client_messages(self, client_username):
        return self._cm.get_client_messages(client_username)

    def set_user_offline(self, client_username):
        return self._cm.set_user_offline(client_username)

    def get_user_status(self, client_username):
        return self._cm.get_user_status(client_username)


class ConvertMixin:
    def _dict_to_bytes(self, messages_dict):
        """Преобразование словаря в байты
        :param messages_dict: dict
        :return bytes"""
        # Проверяем, что пришел словарь
        if isinstance(messages_dict, dict):
            # Преобразуем словарь в json строку
            # json_message = dumps(messages_dict, indent=4, sort_keys=True, default=str)
            json_message = dumps(messages_dict, default=str)
            # json_message = dumps(messages_dict)
            # Преобразуем json строки в байты
            byte_message = json_message.encode(ENCODING)
            return byte_message
        else:
            raise TypeError

    def _bytes_to_dict(self, message_bytes):
        """
        Получение словаря из байтов
        :param message_bytes: сообщение в виде байтов
        :return: словарь сообщения
        """
        # Если переданы байты
        if isinstance(message_bytes, bytes):
            # Декодируем байты
            json_message = message_bytes.decode(ENCODING)
            # Из json получаем словарь
            message = loads(json_message)
            # Если в сообщении словарь
            if isinstance(message, dict):
                # Возвращаем сообщение
                return message
            else:
                # Не верный тип
                raise TypeError
        else:
            # Передан неверный тип
            raise TypeError
