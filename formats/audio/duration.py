import os
from typing import Union

from tinytag import TinyTag

FORMATS = ['mp3', 'ogg', 'opus', 'm4a', 'flac', 'wma']


def format_duration(seconds: int) -> str:
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    if h:
        return f'{h:d}:{m:02d}:{s:02d}'
    elif m:
        return f'{m:02d}:{s:02d}'
    return f'{s:02d} seconds'


def get_file_duration(file_path: str, human: bool = False) -> Union[str, int]:
    """Get duration of an audio file in seconds or in human-readable form."""
    duration = round(TinyTag.get(file_path).duration)
    if human:
        return format_duration(duration)
    return duration


def get_folder_duration(folder_path: str, fmt: str = 'mp3', human=False):
    if fmt:
        audio_files = [
            os.path.join(folder_path, file)
            for file in os.listdir(folder_path)
            if file.lower().endswith(fmt)
        ]
    else:
        audio_files = [
            os.path.join(folder_path, file)
            for file in os.listdir(folder_path)
            if file.lower().rsplit(file, maxsplit=1)[-1] in FORMATS
        ]
    durations = [TinyTag.get(file).duration for file in audio_files]
    total_duration = round(sum(durations))

    if human:
        return format_duration(total_duration)
    return total_duration
