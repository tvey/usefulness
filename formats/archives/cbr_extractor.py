import os

import patoolib
from rarfile import RarFile


def get_folder(file_path: str) -> str:
    """Create a folder with the same name as the file."""
    base_folder = os.path.dirname(file_path)
    name = os.path.splitext(os.path.basename(file_path))[0]
    output_folder = os.path.join(base_folder, name)
    os.makedirs(output_folder, exist_ok=True)
    return output_folder


def extract_cbr(file_path: str, output_folder: str = '') -> None:
    # May require installation of archiving tools like unrar or WinRAR.
    base_folder = os.path.dirname(file_path)
    if not output_folder:
        output_folder = get_folder(file_path)

    with RarFile(file_path) as rf:
        if '/' in rf.namelist()[0] and not output_folder:
            # extract a folder inside without creating an outer folder
            output_folder = base_folder

        for member in rf.namelist():
            rf.extract(member, path=output_folder)

        print(f'Files extracted to "{output_folder}"')


def extract_cbr_patoolib(file_path: str, output_folder: str = ''):
    if not output_folder:
        output_folder = get_folder(file_path)

    patoolib.extract_archive(file_path, outdir=output_folder)
