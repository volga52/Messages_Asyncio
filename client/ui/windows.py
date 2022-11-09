import time
from PyQt5 import QtCore, QtWidgets

from client.ui.login_ui import Ui_Login_Dialog as login_ui_class
from client.ui.chat_ui import Ui_ChatMainWindow as chat_ui_class
from client.ui.contacts_ui import Ui_ContactsWindow as contacts_ui_class


class LoginWindow(QtWidgets.QDialog):
    """Login window (user interface)"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = login_ui_class()
        self.ui.setupUi(self)


class ContactWindow(QtWidgets.QMainWindow):
    """Contacts window (user interface)"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = contacts_ui_class()
        self.ui.setupUi(self)
