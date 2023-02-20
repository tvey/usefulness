import os


def strip_prefix_suffix(root: str, prefix: str = '', suffix: str = '') -> None:
    if (prefix and suffix) or (not prefix and not suffix):
        raise ValueError('Pass either prefix or suffix')

    if prefix:
        files = [
            os.path.join(root, f)
            for f in os.listdir(root)
            if f.startswith(prefix)
        ]
    elif suffix:
        files = [
            os.path.join(root, f)
            for f in os.listdir(root)
            if os.path.splitext(f)[0].endswith(suffix)
        ]

    for file_path in files:
        name, ext = os.path.splitext(os.path.basename(file_path))
        new_name = name.removeprefix(prefix).removesuffix(suffix)
        new_path = os.path.join(root, f'{new_name}{ext}')
        os.rename(file_path, new_path)


def rename_annas_archive_files(root: str) -> None:
    files = [
        os.path.join(root, f) for f in os.listdir(root) if 'annas-archive' in f
    ]

    for file_path in files:
        path = os.path.dirname(file_path)
        old_name, ext = os.path.splitext(os.path.basename(file_path))
        new_name = old_name.split('--')[0].replace('-', ' ').title()
        new_path = os.path.join(path, f'{new_name}{ext}')
        os.rename(file_path, new_path)
