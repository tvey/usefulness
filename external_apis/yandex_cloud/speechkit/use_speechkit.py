import os

import dotenv

from speechkit import SpeechKit

dotenv.load_dotenv()

API_KEY = os.getenv('API_KEY')

sk = SpeechKit(API_KEY)

sk.synthesize('Правда')
sk.synthesize('Truth', lang='en-US', voice='john')
sk.synthesize('Неспеша', voice='filipp', speed='0.5', save_to='audios')
