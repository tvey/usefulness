import os

from pypdf import PdfWriter, PdfReader


def reverse_pdf(file_path):
    path = os.path.dirname(file_path)
    filename = os.path.basename(file_path)
    name, _ = os.path.splitext(filename)
    new_file_path = os.path.join(path, f'{name}_r.pdf')
    writer = PdfWriter()

    with open(file_path, 'rb') as f:
        reader = PdfReader(f)
        total_pages = len(reader.pages)
        for page in range(total_pages - 1, -1, -1):
            writer.add_page(reader.pages[page])
        with open(new_file_path, 'wb') as nf:
            writer.write(nf)

        print(f'File created: {new_file_path}')
