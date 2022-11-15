# import time
from PyQt5 import QtCore, QtWidgets

from client.ui.login_ui import Ui_Login_Dialog as login_ui_class
from client.ui.chat_ui import Ui_ChatMainWindow as chat_ui_class
from client.ui.contacts_ui import Ui_ContactsWindow as contacts_ui_class


class LoginWindow(QtWidgets.QDialog):
    """Login window (user interface)"""

    def __init__(self, auth_instance=None, parent=None):
        super().__init__(parent)

        self.username = None
        self.password = None
        self.auth_instance = auth_instance

        self.ui = login_ui_class()
        self.ui.setupUi(self)

    def on_login_btn_pressed(self):
        """
        Функция обрабатывает ввод логина и пароля
        :return: None
        """
        # Получение из форм логина и пароля
        self.username = self.ui.username_text.text()
        self.password = self.ui.password_text.text()
        # Передаем во внутренние параметры
        self.auth_instance.username = self.username
        self.auth_instance.password = self.password
        # Проверяем полученные элементы по таблице
        is_auth = self.auth_instance.authenticate()
        if is_auth:
            self.accept()
            print(f'{self.username} logged in')
        else:
            self.ui.username_text.clear()
            self.ui.password_text.clear()
            QtWidgets.QMessageBox.warning(self, 'Error',
                                          'Bad user or password')


class ContactWindow(QtWidgets.QMainWindow):
    """Contacts window (user interface)"""

    def __init__(self, client_instance, user_name=None, parent=None):
        super().__init__(parent)
        self.client_instance = client_instance
        self.user_name = user_name
        self.chat_ins = None

        self.ui = contacts_ui_class()
        self.ui.setupUi(self)
