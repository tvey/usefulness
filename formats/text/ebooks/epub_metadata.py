from ebooklib import epub


def process_meta_value(key, metadata):
    value = metadata.get(key)
    if value:
        try:
            items = [i[0] for i in value]
            if len(items) == 1:
                return items[0]
            return items
        except IndexError:
            return ''


def read_meta(file):
    book = epub.read_epub(file)
    book_metadata = book.metadata.get('http://purl.org/dc/elements/1.1/')

    metadata = {
        'Title': book.title,
        'Authors': process_meta_value('creator', book_metadata),
        'Date': process_meta_value('date', book_metadata),
        'Description': process_meta_value('description', book_metadata),
        'UID': book.uid,
        'Language': book.language,
        'Publisher': process_meta_value('publisher', book_metadata),
        'Epub version': book.version,
    }

    for key, value in metadata.items():
        print(f'– {key}: {value}')
