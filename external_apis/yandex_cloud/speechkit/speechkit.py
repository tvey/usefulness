import json
import os

import requests

with open('voices.json') as f:
    VOICES = json.load(f)


class APIException(Exception):
    pass


class SpeechKit:
    """A basic SpeechKit API v1 wrapper for speech synthesis.

    Authenticated using an API key which can be obtained for a service account
    https://cloud.yandex.com/en-ru/docs/iam/operations/api-key/create
    """

    def __init__(self, api_key: str):
        self.api_key = api_key

    def synthesize(
        self,
        text: str,
        voice: str = 'alena',
        emotion: str = 'neutral',
        speed: str = '1.0',
        audio_format: str = 'mp3',
        filename: str = '',
        save_to: str = '.',
    ) -> None:
        """
        Synthesize an audio based on the text and save as an ogg or mp3 file.

        text: limited to 5000 characters.
        voice: https://cloud.yandex.com/en/docs/speechkit/tts/voices.
        emotion: depends on the voice, defaults to 'neutral' for most.
        speed: a decimal number in the range from 0.1 to 3.0.
        audio_format: either mp3 or oggopus are accepted in this wrapper.
        filename: if not passed, defaults to first characters of the text.
        """
        if voice not in VOICES.keys():
            raise ValueError(f'Unsupported voice: {voice}')

        if emotion != 'neutral' or emotion not in VOICES[voice][emotion]:
            raise ValueError(f'Unknown emotion "{emotion}" for voice: {voice}')

        url = 'https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize'
        headers = {'Authorization': f'Api-Key {self.api_key}'}
        data = {
            'text': text,
            'voice': voice,
            'speed': speed,
            'emotion': emotion,
            'format': audio_format,
        }

        r = requests.post(url, headers=headers, data=data)
        if not r.status_code == 200:
            raise APIException(r.json().get('error_message'))

        file_format = 'mp3'

        if audio_format == 'oggopus':
            file_format = 'ogg'

        if not filename:
            safe_chars = [
                i for i in text if i.isalnum() or not i in '\\/:*?"<>|'
            ]
            safe_text = ''.join(safe_chars).strip()
            filename = safe_text[:30]

        if not os.path.exists(save_to):
            raise ValueError('Check "save_to" path, cannot find the directory')

        file_path = os.path.join(save_to, f'{filename}.{file_format}')
        with open(file_path, 'wb') as f:
            f.write(r.content)
