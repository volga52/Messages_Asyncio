from argparse import ArgumentParser
from asyncio import get_event_loop, set_event_loop

from PyQt5 import Qt
from sys import argv
from quamash import QEventLoop

from server.server_config import DB_PATH, PORT
from server.utils.server_proto import ChatServerProtocol
from server.ui.windows import ServerMonitorWindow


class ConsoleServerApp:
    """Console server"""

    def __init__(self, parsed_args, db_path):
        self.args = parsed_args
        self.db_path = db_path
        self.ins = None

    def main(self):
        connections = dict()
        users = dict()
        # Создание основного цикла событий
        loop = get_event_loop()

        # Each client will create a new protocol instance
        # Создание нашего объекта серверного протокола
        self.ins = ChatServerProtocol(self.db_path, connections, users)

        # !корутина! строки 27-32
        # Создание TCP-сервера, встроенными средствами
        coro = loop.create_server(lambda: self.ins,
                                  self.args['addr'],
                                  self.args['port'])
        # Запуск серверного приложения в цикле
        server = loop.run_until_complete(coro)

        # Server requests until Ctrl+C
        print('Server on {}:{}'.format(*server.sockets[0].getsockname()))
        try:
            # Способность реагировать на события по ходу их работы
            loop.run_forever()
        except KeyboardInterrupt:
            pass

        server.close()
        # Постановка задачи в асинхронном процессе:
        # Ожидать окончания работы процесса server
        loop.run_until_complete(server.wait_closed())
        loop.close()


class GuiServerApp:
    """GUI server"""

    def __init__(self, parsed_args, db_path):
        self.args = parsed_args
        self.db_path = db_path
        self.ins = None

    def main(self):
        connections = dict()
        users = dict()

        # Each client will create a new protocol instance
        self.ins = ChatServerProtocol(self.db_path, connections, users)

        # GUI
        app = Qt.QApplication(argv)
        loop = QEventLoop(app)
        # New must set the event loop
        set_event_loop(loop)
        wind = ServerMonitorWindow()
        wind.show()

        with loop:
            coro = loop.create_server(lambda: self.ins,
                                      self.args["addr"],
                                      self.args["port"])
            server = loop.run_until_complete(coro)

            # Server requests until Ctrl+C
            print('Serving on {} {}'.format(*server.sockets[0].getsockname()))
            try:
                loop.run_forever()
            except KeyboardInterrupt:
                pass

            server.close()
            loop.run_until_complete(server.wait_closed())
            loop.close()


def parse_and_run():
    def parse_args():
        parser = ArgumentParser(description="Server setting")
        parser.add_argument("--addr", default="127.0.0.1", type=str)
        parser.add_argument("--port", default=PORT, type=int)
        parser.add_argument("--nogui", action="store_true")
        return vars(parser.parse_args())

    args = parse_args()

    if args['nogui']:
        # start console server
        a = ConsoleServerApp(args, DB_PATH)
        a.main()
    else:
        # Start GUI server
        a = GuiServerApp(args, DB_PATH)
        a.main()


if __name__ == "__main__":
    parse_and_run()
