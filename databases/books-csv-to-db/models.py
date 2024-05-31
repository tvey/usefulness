from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    Float,
    DateTime,
    Table,
    Text,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

book_author = Table(
    'book_author',
    Base.metadata,
    Column('book_id', Integer, ForeignKey('books.id'), primary_key=True),
    Column('author_id', Integer, ForeignKey('authors.id'), primary_key=True),
)


class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    middle_name = Column(String)
    url = Column(String)

    books = relationship(
        'Book',
        secondary=book_author,
        back_populates='authors',
    )

    def __repr__(self):
        return f'Author(id={self.id}, last_name={self.last_name})'


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    slug = Column(String)
    url = Column(String)  # == slug

    books = relationship('Book', back_populates='category')

    def __repr__(self):
        return f'Category(id={self.id}, title={self.title})'


class Publisher(Base):
    __tablename__ = 'publishers'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    slug = Column(String)

    books = relationship('Book', back_populates='publisher')

    def __repr__(self):
        return f'Publisher(id={self.id}, title={self.title})'


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    url = Column(Text)
    year_published = Column(Integer)
    description = Column(Text)
    picture = Column(String)
    original_picture = Column(String)
    rating = Column(Float)
    rating_votes = Column(Integer)
    code = Column(Integer)  # == id
    status = Column(String)
    bestseller = Column(Boolean)
    new = Column(Boolean)
    recommended = Column(Boolean)
    exclusive = Column(Boolean)
    price = Column(Integer)
    old_price = Column(Integer)
    discount = Column(Integer)
    sale = Column(Boolean)
    sale_soon = Column(String)
    sale_start = Column(String)
    sale_start_desc = Column(String)
    pre_order_date = Column(DateTime(timezone=True))
    is_book = Column(Boolean)
    is_bookmark = Column(Boolean)
    in_subscription = Column(Boolean)
    pages = Column(Integer)
    binding = Column(String)
    category_id = Column(Integer, ForeignKey('categories.id'))
    publisher_id = Column(Integer, ForeignKey('publishers.id'))

    authors = relationship(
        'Author',
        secondary=book_author,
        back_populates='books',
    )
    category = relationship('Category', back_populates='books')
    publisher = relationship('Publisher', back_populates='books')

    def __repr__(self):
        return f'Book(id={self.id}, title={self.title})'
