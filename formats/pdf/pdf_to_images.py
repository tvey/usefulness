# poppler is required: https://github.com/Belval/pdf2image

import os
import tempfile

import pdf2image


def convert_pdf_to_images(file_path: str) -> None:
    directory = os.path.dirname(file_path)
    name = os.path.basename(file_path).rsplit('.')[0]
    new_folder = os.path.join(directory, name)
    os.makedirs(new_folder, exist_ok=True)

    num_pages = pdf2image.pdfinfo_from_path(file_path).get('Pages')

    with tempfile.TemporaryDirectory() as tempdir:
        for page in range(1, num_pages + 1):
            image = pdf2image.convert_from_path(
                file_path,
                dpi=300,
                fmt='jpeg',
                first_page=page,
                last_page=page,
                output_folder=tempdir,
            )[0]

            image.save(f'{new_folder}/page_{page:03}.jpg', 'JPEG')
            print(f'Saved page {page:03}/{num_pages}')

if __name__ == '__main__':
    convert_pdf_to_images('/home/tanya/Books/Various/Flora Inside the Secret World of Plants by DK.pdf')
