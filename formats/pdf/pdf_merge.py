import logging
import os

from PyPDF2 import PdfFileReader, PdfFileWriter
from PyPDF2.errors import PyPdfError

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(message)s',
    # filename='pdf_merge.log',
)
logger = logging.getLogger(__name__)


def merge_pdfs(file_paths: list[str], output_filename: str, save_to: str = '.'):
    pdfs = [
        file
        for file in file_paths
        if os.path.isfile(file) and file.lower().endswith('.pdf')
    ]
    if not pdfs:
        logging.info('Nothing to merge, zero PDFs provided')
        return

    pdfs.sort(key=str.lower)
    logger.info(f'Merging {len(pdfs)} files')
    pdf_writer = PdfFileWriter()

    for path in pdfs:
        try:
            pdf_reader = PdfFileReader(path)
            logger.info(f'Adding: {os.path.basename(path)}')
            for page in range(pdf_reader.numPages):
                pdf_writer.addPage(pdf_reader.getPage(page))
        except PyPdfError:
            logging.error(f'Unable to merge file {path}. Skipping')

    with open(f'{save_to}/{output_filename}.pdf', 'wb') as f:
        pdf_writer.write(f)

    logger.info(f'File ready: {save_to}/{output_filename}.pdf')


def merge_folder(folder: str, output_filename: str, save_to: str = '.'):
    files = [
        os.path.join(folder, file)
        for file in os.listdir(folder)
        if os.path.isfile(os.path.join(folder, file))
    ]
    merge_pdfs(files, output_filename, save_to)
