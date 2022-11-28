from pikepdf import Pdf
from PyPDF2 import PdfFileReader


def read_meta_pypdf2(file_path):
    with open(file_path, 'rb') as f:
        pdf = PdfFileReader(f)
        info = dict(pdf.documentInfo)
        num_pages = pdf.numPages
        info['Number of pages'] = num_pages

    for key, value in info.items():
        print(f'– {key.strip("/")}: {value}')

    return info


def read_meta_pikepdf(file_path):
    pdf = Pdf.open(file_path)
    info = pdf.docinfo
    info['/Number of pages'] = len(pdf.pages)

    for key, value in info.items():
        print(f'– {key.strip("/")}: {value}')

    return info
