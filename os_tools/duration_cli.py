"""Get duration info about folder with videos."""

import argparse
import datetime
import os

import humanize
from tinytag import TinyTag


class Folder:
    supported_formats = ('mp4', 'mkv', 'avi', 'mov', 'wmv', 'webm')

    def __init__(self, path: str):
        self.path = path

    def __repr__(self):
        return f'Folder({self.path})'

    @property
    def subfolders(self) -> list[str]:
        """Get immediate children folders."""
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
    def videos(self) -> list[str]:
        """Get full paths of videos inside the folder."""
        return [i for i in self.files if i.endswith(self.supported_formats)]

    def get_size(self, human: bool = False) -> int | str:
        """Get total size, bytes or human-readable."""
        total_size = 0
        for file_path in self.files:
            total_size += os.path.getsize(file_path)
        if human:
            return humanize.naturalsize(total_size)
        return total_size

    def get_duration(self, human=False) -> int | str:
        """Get total duration, seconds (int) or human-readable."""
        duration = 0
        for file in self.videos:
            duration += TinyTag.get(file).duration
        if human:
            return str(datetime.timedelta(seconds=duration)).split('.')[0]
        return duration

    @property
    def duration(self) -> str:
        """Folder duration in human-readable format."""
        return self.get_duration(human=True)


def main():
    parser = argparse.ArgumentParser(
        description='Get total duration of videos in a folder'
    )
    parser.add_argument('folder', help='Folder path')
    args = parser.parse_args()

    folder = Folder(args.folder)
    total_duration = folder.get_duration(human=True)
    number_of_videos = len(folder.videos)

    if number_of_videos:
        average_duration_seconds = folder.get_duration() / number_of_videos
        average_duration = str(
            datetime.timedelta(seconds=average_duration_seconds)
        ).split('.')[0]
    else:
        average_duration = '0'

    print(
        f'Total duration: {total_duration}\n'
        f'Number of videos: {number_of_videos}\n'
        f'Average video duration: {average_duration}'
    )


if __name__ == '__main__':
    main()
