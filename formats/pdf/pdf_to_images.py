import os

import pdf2image


def convert_pdf_to_image(file_path):
    directory = os.path.dirname(file_path)
    name = os.path.basename(file_path).rsplit('.')[0]
    new_folder = os.path.join(directory, name)
    os.makedirs(new_folder, exist_ok=True)

    images = pdf2image.convert_from_path(file_path)

    for i, image in enumerate(images):
        image.save(f'{new_folder}/page_{i:03}.jpg', 'JPEG')
