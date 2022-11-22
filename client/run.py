from argparse import ArgumentParser
from asyncio import ensure_future, get_event_loop, run, create_task, \
    set_event_loop
from sys import argv
from sys import exit as sys_exit

from PyQt5 import Qt, QtWidgets
# from PyQt5 import QtWidgets

from quamash import QEventLoop

from client.ui.windows import LoginWindow, ContactsWindow
from client.utils.client_proto import ChartClientProtocol, ClientAuth
from client.client_config import DB_PATH, PORT


class ConsoleClientApp:
    """Console client"""

    def __init__(self, parsed_args, db_path):
        self.args = parsed_args
        self.db_path = db_path
        self.ins = None

    def main(self):
        # create event loop (текущий цикл событий)
        loop = get_event_loop()

        # authentication process
        auth = ClientAuth(db_path=self.db_path)
        while True:
            _user = self.args["user"] or input("username: ")
            password = self.args["password"] or input("password")
            auth.username = _user
            auth.password = password
            is_auth = auth.authenticate()
            if is_auth:
                break
            else:
                print("wrong username/password")

        tasks = []
        _client = ChartClientProtocol(db_path=self.db_path,
                                      loop=loop,
                                      username=_user,
                                      password=password)
        try:
            coro = loop.create_connection(lambda: _client, self.args["addr"],
                                          self.args["port"])
            transport, protocol = loop.run_until_complete(coro)

        except ConnectionRefusedError:
            print('Error. wrong server')
            sys_exit(1)
            # exit(1)

        try:
            task = loop.create_task(_client.get_from_console())
            tasks.append(task)
            loop.run_until_complete(task)
        except KeyboardInterrupt:
            pass
        except Exception as e:
            print(e)

        finally:
            loop.close()


class GuiClientApp:
    """GUI client"""
    def __init__(self, parsed_args, db_path):
        self.args = parsed_args
        self.db_path = db_path
        self.ins = None

    def main(self):
        """Основная функция запуска GUI client"""
        # create event loop
        # app = Qt.QApplication(argv)
        app = QtWidgets.QApplication(argv)
        loop = QEventLoop(app)
        # New must set the event loop
        set_event_loop(loop)

        # authentication process
        auth_ = ClientAuth(db_path=self.db_path)
        login_window = LoginWindow(auth_instance=auth_)

        # Отлов подтверждения
        # if login_window.exec_() == QtWidgets.QDialog.Accepted:
        # if login_window.exec_() == QDialog.Accepted:
        if login_window.exec_() == QtWidgets.QDialog.Accepted:
            # Each client will create a new protocol instance
            client_ = ChartClientProtocol(db_path=self.db_path,
                                          loop=loop,
                                          username=login_window.username,
                                          password=login_window.password)
            # Create Contacts window
            window = ContactsWindow(client_instance=client_,
                                    user_name=login_window.username)
            # reference from protocol to GUI, for msg update
            # ссылка из протокола на графический интерфейс пользователя
            # для обновления msg
            client_.gui_instance = window

            with loop:
                # cleaning old instances
                del auth_
                del login_window

                # connect to our server
                try:
                    coro = loop.create_connection(lambda: client_,
                                                  self.args['addr'],
                                                  self.args['port'])
                    server = loop.run_until_complete(coro)
                except ConnectionRefusedError:
                    print('Error. wrong server')
                    exit(1)

                # start GUI client
                window.show()
                # asyncio.ensure_future(client_.get_from_gui(loop))
                # client_.get_from_gui()

                # server requests until Ctrl+C
                try:
                    loop.run_forever()
                except KeyboardInterrupt:
                    pass
                except Exception:
                    pass


def parse_and_run():
    def parse_args():
        parser = ArgumentParser(description="Client settings")
        parser.add_argument("--user", default="user1", type=str)
        parser.add_argument("--password", default="123", type=str)
        parser.add_argument("--addr", default="127.0.0.1", type=str)
        parser.add_argument("--port", default=PORT, type=int)
        parser.add_argument('--nogui', action='store_true')
        return vars(parser.parse_args())

    args = parse_args()

    if args['nogui']:
        # start consoles server
        a = ConsoleClientApp(args, DB_PATH)
        a.main()
    else:
        # start GUI server
        a = GuiClientApp(args, DB_PATH)
        a.main()


if __name__ == '__main__':
    parse_and_run()
