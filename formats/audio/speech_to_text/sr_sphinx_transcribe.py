# ffmpeg and CMUSphinx are required

import os

from speech_recognition import Recognizer, AudioFile
from pydub import AudioSegment

audio_file_path = ''


def transcribe(mp3_file_path: str, save_to_file: bool = True) -> str:
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
        transcript = r.recognize_sphinx(record)

    if save_to_file:
        transcript_path = os.path.join(folder, f'{name}.txt')
        with open(transcript_path, 'w', encoding='utf-8') as f:
            f.write(transcript)
        print(f'Transcription saved: {transcript_path}')

    return transcript


if __name__ == '__main__':
    transcribe(audio_file_path)
