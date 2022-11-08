from datetime import datetime


class JimClientMessage:
    def auth(self, username, password):
        """
        Authorization message
        :param user:
        :param password:
        :return: dict with data
        """
        data = {
            'action': 'authenticate',
            'time': datetime.now().timestamp(),
            'type': 'status',
            'user': {
                'account_name': username,
                'password': password
            }
        }
        return data

    def response(self, code=None, error=None):
        _data = {
            'action': 'response',
            'code': code,
            'time': datetime.now(),
            'error': error
        }
        return _data

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

