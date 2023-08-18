import os


def move_file_to_same_name_folder(file_path: str):
    """Accept a full file path, move the file into a eponymous folder."""
    if not os.path.isfile(file_path):
        raise ValueError('File path is incorrect')

    parent_folder, filename = os.path.split(file_path)
    name, ext = os.path.splitext(filename)
    new_path = os.path.join(parent_folder, name)
    new_file_path = os.path.join(new_path, filename)
    os.makedirs(new_path, exist_ok=True)

    try:
        os.rename(file_path, new_file_path)
        print(f'Moved: {new_file_path}')
    except FileExistsError:
        duplicate_filename = f'{name} (duplicate){ext}'
        duplicate_path = os.path.join(parent_folder, duplicate_filename)
        os.rename(file_path, duplicate_path)

        move_file_to_same_name_folder(duplicate_path)


def move_files_from_subfolders(root: str):
    pass