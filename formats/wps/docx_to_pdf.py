import os

from docx2pdf import convert


def convert_files(folder: str) -> None:
    """Convert docx files found in the folder and save in the same place."""
    docs = [
        os.path.join(folder, file)
        for file in os.listdir(folder)
        if file.endswith('docx')
    ]

    if docs:
        print(f'Converting {len(docs)} files')
        for doc in docs:
            path, _ = os.path.splitext(doc)
            pdf = f'{path}.pdf'
            print(f'{os.path.basename(doc)} --> {os.path.basename(pdf)}')
            convert(doc, pdf)
