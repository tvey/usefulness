# ffmpeg required

import os

import whisper

audio_file_path = ''


def transcribe(audio_file_path):
    path = os.path.dirname(audio_file_path)
    name = os.path.splitext(os.path.basename(audio_file_path))[0]
    transcribe_path = os.path.join(path, f'{name}.txt')
    model = whisper.load_model('base')
    result = model.transcribe(audio_file_path)

    with open(transcribe_path, 'w', encoding='utf-8') as f:
        f.write(result['text'])


if __name__ == '__main__':
    transcribe(audio_file_path)
