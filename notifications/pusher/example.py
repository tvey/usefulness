import os
import time

import dotenv
import schedule
from pusher import Pusher

dotenv.load_dotenv()

user = os.environ.get('USER_KEY')
token = os.environ.get('APP_TOKEN')

pusher = Pusher(user=user, token=token)


def annoy():
    """Send a reminder message to Pushover client(s)."""
    message = "You know it's time."
    pusher.send(message)


schedule.every().hour.do(annoy)

while True:
    schedule.run_pending()
    time.sleep(1)
