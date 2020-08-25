from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy

Base = declarative_base()

class Publisher(Base):
    __tablename__ = 'publisher'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    books = relationship('Book', back_populates='publisher')


class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    id_publisher = Column(Integer, ForeignKey('publisher.id'))
    publisher = relationship('Publisher', back_populates='books')
    stocks = relationship('Stock', back_populates='book')


class Shop(Base):
    __tablename__ = 'shop'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    stocks = relationship('Stock', back_populates='shop')


class Stock(Base):
    __tablename__ = 'stock'
    id = Column(Integer, primary_key=True)
    id_book = Column(Integer, ForeignKey('book.id'))
    book = relationship('Book', back_populates='stocks')
    id_shop = Column(Integer, ForeignKey('shop.id'))
    shop = relationship('Shop', back_populates='stocks')
    count = Column(Integer)
    sales = relationship('Sale', back_populates='stock')


class Sale(Base):
    __tablename__ = 'sale'
    id = Column(Integer, primary_key=True)
    price = Column(Numeric(15, 2), nullable=False)
    date_sale = Column(DateTime)
    id_stock = Column(Integer, ForeignKey('stock.id'))
    stock = relationship('Stock', back_populates='sales')
    count = Column(Integer, nullable=False)


def create_md(psql_engine: sqlalchemy.engine):
    Base.metadata.create_all(psql_engine)


if __name__ == '__main__':
    engine = create_engine('postgresql://Pushkin:1@localhost/BookStore')
    create_md(engine)
