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


class ContactsWindow(QtWidgets.QMainWindow):
    """Contacts window (user interface)"""

    def __init__(self, client_instance, user_name=None, parent=None):
        super().__init__(parent)

        self.client_instance = client_instance
        self.username = user_name
        self.chat_ins = None

        self.ui = contacts_ui_class()
        self.ui.setupUi(self)

        self.ui.actionExit.triggered.connect(self.actionExit)

        self.after_start()

    def closeEvent(self, event):
        self.client_instance._cm.dal.session.close()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Enter:
            # here accept the event and do something
            self.on_add_new_contact_btn_pressed()
            event.accept()
        else:
            event.ignore()

    def after_start(self):
        self.update_contacts(self.username)

    def update_contacts(self, client_username):
        contacts = self.client_instance.get_contacts(client_username)
        self.ui.all_contacts.clear()
        self.ui.all_contacts.addItems(
            [contact.contact.username for contact in contacts])

    def on_add_new_contact_btn_pressed(self):
        contact_username = self.ui.new_contact_name.text()

        if contact_username:
            _resp = self.client_instance.add_contact(self.username,
                                                     contact_username)
            if not _resp:
                self.update_contacts(self.username)
                self.ui.new_contact_name.clear()
            else:
                print(_resp)
        else:
            QtWidgets.QMessageBox.warning(self, 'Error', 'wrong Name')

    def on_delete_contact_btn_pressed(self):
        try:
            selected_contact = self.ui.all_contacts.currentItem().text()
            _resp = self.client_instance.del_contact(self.username,
                                                     selected_contact)

            if not _resp:

                self.update_contacts(self.username)
            else:
                print(_resp)

        except AttributeError:
            QtWidgets.QMessageBox.warning(self, 'Error',
                                          'Please pick the contact')

    def on_all_contacts_itemDoubleClicked(self):
        chat_wnd = ChatWindow(self)
        chat_wnd.show()

    def actionExit(self):
        self.close()


class ChatWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = chat_ui_class()
        self.ui.setupUi(self)
        self.parent_window = parent

        # self.after_start()
