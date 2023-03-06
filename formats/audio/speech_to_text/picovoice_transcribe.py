import os

import pvleopard
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

access_key = os.getenv('PICOVOICE_ACCESS_KEY')
audio_file_path = ''


def transcribe(audio_file_path: str, save_to_file: bool = True) -> str:
    leopard = pvleopard.create(access_key=access_key)
    transcript, words = leopard.process_file(audio_file_path)

    folder = os.path.dirname(audio_file_path)
    filename = os.path.basename(audio_file_path)
    name = os.path.splitext(filename)[0]
    transcript_path = os.path.join(folder, f'{name}.txt')

    if save_to_file:
        transcript_path = os.path.join(folder, f'{name}.txt')
        with open(transcript_path, 'w', encoding='utf-8') as f:
            f.write(transcript)
        print(f'Transcription saved: {transcript_path}')

    return transcript


if __name__ == '__main__':
    transcribe(audio_file_path)
