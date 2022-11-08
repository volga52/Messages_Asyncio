from datetime import datetime


class JimServerMessage:
    def probe(self, sender, status='Are you there?'):
        data = {
            'action': 'probe',
            'time': datetime.now().timestamp(),
            'type': 'status',
            'user': {
                'account_name': sender,
                'status': status
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