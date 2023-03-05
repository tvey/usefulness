# ffmpeg and CMUSphinx are required

import os

from speech_recognition import Recognizer, AudioFile
from pydub import AudioSegment

AUDIO_FILE_PATH = 'sample.mp3'


def recognize(mp3_file_path: str) -> None:
    folder = os.path.dirname(mp3_file_path)
    filename = os.path.basename(mp3_file_path)
    name = os.path.splitext(filename)[0]
    wav_filename = f'{name}.wav'
    wav_file_path = os.path.join(folder, wav_filename)

    audio = AudioSegment.from_mp3(mp3_file_path)
    audio.export(wav_file_path, format='wav')

    r = Recognizer()
    with AudioFile(wav_file_path) as audio_file:
        record = r.record(audio_file)
        transcription = r.recognize_sphinx(record)
        transcription_path = os.path.join(folder, f'{name}.txt')

        with open(transcription_path, 'w', encoding='utf-8') as f:
            f.write(transcription)

        print(f'Transcription saved: {transcription_path}')


if __name__ == '__main__':
    recognize(AUDIO_FILE_PATH)
