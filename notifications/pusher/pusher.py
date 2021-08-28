"""Simple wrapper class for Pushover API — https://pushover.net/api"""

import requests

BASE_URL = 'https://api.pushover.net/1/'
MESSAGE_URL = BASE_URL + 'messages.json'


class Pusher:
    """Simplified notification sender."""

    def __init__(self, user, token):
        self.user = user
        self.token = token

        self.message_params = [
            'title',
            # more to be added
        ]

    def send(self, message, **params):
        data = {
            'user': self.user,
            'token': self.token,
            'message': message,
        }

        for k, v in params.items():
            if k in self.message_params:
                data[k] = v

        r = requests.post(MESSAGE_URL, data=data)

        if not r.status_code == requests.codes.ok:
            return False
        return True
