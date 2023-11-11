"""Folder class calculates total duration of selected media files
and total folder size in human-readable format or in ints of seconds/bytes.
"""
import datetime
import os

import humanize
from tinytag import TinyTag


class Folder:
    supported_formats = ('mp4', 'mp3', 'flac')

    def __init__(self, path: str):
        self.path = path

    def __repr__(self):
        return f'Folder({self.path})'

    @property
    def subfolders(self) -> list[str]:
        """Immediate children folders."""
        return [i.path for i in os.scandir(self.path) if i.is_dir()]

    @property
    def files(self) -> list[str]:
        """List full paths to files in folder and subfolders."""
        file_paths = []
        for root, subs, files in os.walk(self.path):
            for file in files:
                file_path = os.path.join(os.path.abspath(root), file)
                if not os.path.islink(file_path):
                    file_paths.append(file_path)
        return file_paths

    @property
    def media_files(self) -> list[str]:
        """List full paths of selected files."""
        return [i for i in self.files if i.endswith(self.supported_formats)]

    def get_size(self, human: bool = False) -> int | str:
        """Get total size, bytes or human-readable."""
        total_size = 0

        for file_path in self.files:
            total_size += os.path.getsize(file_path)

        if human:
            return humanize.naturalsize(total_size)
        return total_size

    @property
    def size(self) -> str:
        """Folder size in human-readable format."""
        return self.get_size(human=True)

    def get_duration(self, human=False) -> int | str:
        """Get total duration, seconds (int) or human-readable."""
        duration = 0
        for file in self.media_files:
            duration += TinyTag.get(file).duration
        if human:
            return str(datetime.timedelta(seconds=duration)).split('.')[0]
        return duration

    @property
    def duration(self) -> str:
        """Folder duration in human-readable format."""
        return self.get_duration(human=True)
