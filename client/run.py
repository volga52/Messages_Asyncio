from argparse import ArgumentParser
from asyncio import ensure_future, get_event_loop, run, create_task

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
            exit(1)

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


if __name__ == '__main__':
    parse_and_run()
