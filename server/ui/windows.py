from PyQt5.QtWidgets import QMainWindow
from server.ui.server_monitor import Ui_ServerWindow as server_ui_class


class ServerMonitorWindow(QMainWindow):
    """Server Monitor Window (user interface)"""
    # , parsed_args, server_instance
    def __init__(self, parsed_args, server_instance, parent=None):
        super().__init__(parent)
        self.server_instance = server_instance
        self.parsed_args = parsed_args

        self.ui = server_ui_class()
        self.ui.setupUi(self)
        self.ui.refresh_action.triggered.connect(self.refresh_action)
        self.after_start()

    def closeEvent(self, event):
        """
        Close DB connection before exit (close window)
        :param event:
        :return:
        """
        self.server_instance._cm.dal.session.close()  # close DB connection

    def after_start(self):
        """do appropriate things after starting the App"""

        self.update_clients()

    def update_clients(self):
        """Update clients list"""

        contacts = self.server_instance.get_all_clients()
        self.ui.clients_list.clear()
        self.ui.clients_list.addItems(
            [contact.username for contact in contacts])

    def refresh_action(self):
        """refresh from menu
        QAction.triggered only work with direct connect() method,
        otherwise it will be triggered twice."""

        print('refresh')
        self.update_clients()