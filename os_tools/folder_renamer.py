import os


def rename_folder(folder_path: str, new_name: str) -> None:
    parent_folder = os.path.dirname(folder_path)
    new_path = os.path.join(parent_folder, new_name)
    try:
        os.rename(folder_path, new_path)
    except FileExistsError:
        new_name = f'{new_name} (duplicate)'

    print(f'Renamed {folder_path} to {new_path}')


def strip_prefix_suffix(
    folder_path: str, prefix: str = None, suffix: str = None
) -> None:
    new_name = ''
    folder_name = os.path.basename(folder_path)

    if prefix and suffix:
        raise ValueError('Pass either prefix or suffix')

    if prefix and folder_name.startswith(prefix):
        new_name = folder_name.replace(prefix, '').strip()
    elif suffix and folder_name.endswith(suffix):
        new_name = folder_name.replace(suffix, '').strip()

    if new_name:
        rename_folder(folder_path, new_name)
