import os
import tempfile

import pdf2image


def save_cover_as_image(pdf_file_path: str, output_folder: str = '') -> None:
    if not os.path.isfile(pdf_file_path):
        raise ValueError(f'Cannot find the file: {pdf_file_path}')
    if output_folder and not os.path.isdir(output_folder):
        raise ValueError(f'Cannot find the folder: {output_folder}')
    if not output_folder:
        output_folder = os.path.dirname(pdf_file_path)

    pdf_filename = os.path.basename(pdf_file_path)
    name = os.path.splitext(pdf_filename)[0]

    with tempfile.TemporaryDirectory() as tempdir:
        image = pdf2image.convert_from_path(
            pdf_file_path,
            dpi=600,
            fmt='jpeg',
            first_page=1,
            last_page=1,
            output_folder=tempdir,
        )[0]

        image_path = os.path.join(output_folder, f'{name}.jpg')
        image.save(image_path, 'JPEG')
        print(f'Saved: {image_path}')
