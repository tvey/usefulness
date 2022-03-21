import argparse
import os


def remove_files(root: str, extensions: list):
    """Remove files with selected extensions from a root or all subfolders."""
    counter = 0
    for currentpath, folders, files in os.walk(root):
        files_to_remove = [
            f for f in files if f.rsplit('.', 1)[-1] in extensions
        ]
        for file in files_to_remove:
            os.remove(os.path.join(currentpath, file))
            counter += 1
    print(f'Removed {counter} files!')


parser = argparse.ArgumentParser(
    prog='File Remover',
    usage='%(prog)s [options] root extensions',
    description='Remove unneeded files from a folder and subfilders.',
)

parser.add_argument(
    'root',
    help='Local path to a directory to be cleaned.',
)

parser.add_argument(
    '-e',
    nargs='*',
    help='Extensions of files to remove. Example: -e txt srt vtt',
)


if __name__ == '__main__':
    args = parser.parse_args()
    remove_files(args.root, args.e)
