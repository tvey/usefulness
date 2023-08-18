import argparse
import os

import humanize


class Folder:
    def __init__(self, path: str):
        self.path = path

    def __repr__(self):
        return f'Folder("{self.path}")'

    @property
    def files(self) -> list[str]:
        """List of full paths to files in folder and subfolders."""
        file_paths = []

        for root, subs, files in os.walk(self.path):
            for file in files:
                file_path = os.path.join(os.path.abspath(root), file)
                if not os.path.islink(file_path):
                    file_paths.append(file_path)
        return file_paths

    def get_sizes(self):
        sizes = []

        for file_path in self.files:
            file_size = os.path.getsize(file_path)
            sizes.append((file_path, file_size))

        return sorted(sizes, key=lambda i: i[1], reverse=True)

    def format_line(self, value):
        """Format one size-path pair for output for output."""
        size = humanize.naturalsize(value[1], format='%.1f')
        return f'{size.ljust(12)}{value[0]}'

    def top(self, num=10):
        try:
            num = int(num)
        except ValueError as e:
            print(e)

        file_sizes = self.get_sizes()[:num]
        return '\n'.join([self.format_line(i) for i in file_sizes])


def show_files(root, num=10):
    folder = Folder(root)
    print(folder.top(num=num))


parser = argparse.ArgumentParser(
    prog='File sizes',
    usage='%(prog)s [options] root -num',
    description='Remove unneeded files from a folder and subfolders.',
)

parser.add_argument(
    'root',
    help='Local path to a directory.',
)

parser.add_argument(
    '-num',
    nargs='?',
    default=10,
    help='Number of biggest files to display.',
)


if __name__ == '__main__':
    args = parser.parse_args()
    show_files(args.root, args.num)
