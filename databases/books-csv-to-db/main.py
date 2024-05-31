import os
import time
from concurrent.futures import ThreadPoolExecutor

import numpy as np
import pandas as pd
from dateutil import parser
from dotenv import load_dotenv
from sqlalchemy import create_engine, insert, select
from sqlalchemy.orm import sessionmaker

from models import Base, Author, Book, Category, Publisher

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine, expire_on_commit=False)


def conv_type(value, to='str'):
    if isinstance(value, str):
        value = value.strip(' .,')

    if value in [None, '', 'None', 'nan', 'null', 0, '0']:
        return None

    if to == 'date':
        return parser.parse(value)

    conversion_map = {
        'int': int,
        'float': float,
        'str': str,
    }

    try:
        conv = conversion_map.get(to)
        if conv:
            # print(f'Converting {value} ({type(value)}) to {to}')
            return conv(value)
        else:
            raise ValueError(f'Unsupported type: {to}')
    except ValueError as e:
        raise ValueError(f'Conversion error: {e} for value {value}')


def get_or_create_author(session, author_data):
    query = select(Author).where(Author.id == author_data.get('id'))
    author = session.execute(query).scalar_one_or_none()

    if not author:
        author = Author(**author_data)
        session.add(author)
        session.commit()
        session.refresh(author)
    return author


def extract_authors(session, row):
    authors = []
    for i in range(1, 5):
        author_id = row.get(f'authors_{i}_id')
        if author_id:
            author_data = {
                'id': int(author_id),
                'first_name': conv_type(
                    row.get(f'authors_{i}_firstName'), to='str'
                ),
                'last_name': conv_type(
                    row.get(f'authors_{i}_lastName'), to='str'
                ),
                'middle_name': conv_type(
                    row.get(f'authors_{i}_middleName'), to='str'
                ),
                'url': conv_type(row.get(f'authors_{i}_url'), to='str'),
            }
            authors.append(get_or_create_author(session, author_data))
    return authors


def get_or_create_category(session, row):
    category_id = row.get('category_id')

    if category_id:
        query = select(Category).where(Category.id == int(category_id))
        category = session.execute(query).scalar_one_or_none()

        if not category:
            category_data = {
                'id': int(category_id),
                'title': conv_type(row.get('category_title'), to='str'),
                'slug': conv_type(row.get('category_slug'), to='str'),
                'url': conv_type(row.get('category_url'), to='str'),
            }
            category = Category(**category_data)
            session.add(category)
            session.commit()
            session.refresh(category)
            print('Created category:', category)
        return category


def get_or_create_publisher(session, row):
    publisher_id = row.get('publisher_id')

    if publisher_id:
        query = select(Publisher).where(Publisher.id == int(publisher_id))
        publisher = session.execute(query).scalar_one_or_none()

        if not publisher:
            publisher_data = {
                'id': int(publisher_id),
                'title': conv_type(row.get('publisher_title'), to='str'),
                'slug': conv_type(row.get('publisher_slug'), to='str'),
            }
            publisher = Publisher(**publisher_data)
            session.add(publisher)
            session.commit()
            session.refresh(publisher)
            print('Created publisher:', publisher)
        return publisher


def process_book_row(session, row):
    book_data = {
        'id': conv_type(row.get('id'), to='int'),
        'title': conv_type(row.get('title'), to='str'),
        'url': conv_type(row.get('url'), to='str'),
        'year_published': conv_type(row.get('yearPublishing'), to='int'),
        'description': conv_type(row.get('description'), to='str'),
        'picture': conv_type(row.get('picture'), to='str'),
        'original_picture': conv_type(row.get('originalPicture'), to='str'),
        'rating': conv_type(row.get('rating_count'), to='float'),
        'rating_votes': conv_type(row.get('rating_votes'), to='int'),
        'code': conv_type(row.get('code'), to='int'),
        'status': conv_type(row.get('status'), to='str'),
        'bestseller': row.get('bestseller'),
        'new': row.get('new'),
        'recommended': row.get('recommended'),
        'exclusive': row.get('exclusive'),
        'price': conv_type(row.get('price'), to='int'),
        'old_price': conv_type(row.get('oldPrice'), to='int'),
        'discount': conv_type(row.get('discount'), to='int'),
        'sale': row.get('sale'),
        'sale_soon': row.get('saleSoon'),
        'sale_start': conv_type(row.get('startSale'), to='str'),
        'sale_start_desc': row.get('startSaleDesc'),
        'pre_order_date': conv_type(row.get('preOrderDate'), to='date'),
        'is_book': row.get('isBook'),
        'is_bookmark': row.get('isBookmarks'),
        'in_subscription': row.get('inSubscription'),
        'pages': conv_type(row.get('pages'), to='int'),
        'binding': conv_type(row.get('binding'), to='str'),
    }
    book = Book(**book_data)
    authors = extract_authors(session, row)
    category = get_or_create_category(session, row)
    publisher = get_or_create_publisher(session, row)

    if authors:
        book.authors = authors
    if category:
        book.category_id = category.id
        book.category = category
    if publisher:
        book.publisher_id = publisher.id
        book.publisher = publisher

    print(f'-----------\nBOOK obj:', book)
    session.add(book)
    # session.commit()
    return book


def process_file(filepath):
    session = Session()
    try:
        df = pd.read_csv(filepath)
        df.replace('', None, inplace=True)
        df = df.replace(np.nan, None)

        books = []
        for _, row in df.iterrows():
            books.append(process_book_row(session, row))
            session.commit()
            books.clear()
        if books:
            session.commit()

    except Exception as e:
        print(f'An error occurred: {e}')
        session.rollback()
    finally:
        session.close()


def main(files_root):
    files = [
        os.path.join(files_root, f)
        for f in os.listdir(files_root)
        if f.endswith('.csv')
    ]
    t1 = time.time()
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(process_file, files)
    print(time.time() - t1)


if __name__ == '__main__':
    main('example_csv')
