"""Folder class that calculates total duration of selected media files.
For now...
"""

import os
import datetime

from tinytag import TinyTag


class Folder:
    supported_formats = ('mp4', 'mp3', 'flac')

    def __init__(self, path):
        self.path = path

    def __repr__(self):
        return f'Folder({self.path})'

    @property
    def subfolders(self):
        """Immediate children folders."""
        return [i.path for i in os.scandir(self.path) if i.is_dir()]

    @property
    def files(self):
        """List full paths of selected files."""
        file_paths = []
        for root, subs, files in os.walk(self.path):
            for file in files:
                if file.endswith(self.supported_formats):
                    file_path = os.path.join(os.path.abspath(root), file)
                    file_paths.append(file_path)
        return file_paths

    def get_duration(self, human=False):
        """Get total duration of files, human-readable or timedelta."""
        duration = 0
        for file in self.files:
            duration += TinyTag.get(file).duration
        if human:
            return str(datetime.timedelta(seconds=duration)).split('.')[0]
        return duration

    @property
    def duration(self):
        """Display duration in human-readable format."""
        return self.get_duration(human=True)
