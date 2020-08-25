from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from db_definition import Publisher, Stock, Shop, Book
from sqlalchemy import func,or_

def find_shops_by_publisher(session, publ_name):
    try:
        publ_id = int(publ_name)
    except ValueError:
        publ_id = None

    # select * from shop
    # where id in (
    #   select stock.id_shop from stock
    #   where stock.id_book in (
    #       select book.id from book join publisher on book.id_publisher = publisher.id
    #       where publisher.name = {publisher_name} or publisher.id = {publisher_id}
    #   )
    #   group by stock.id_shop
    #   having sum(count)>0
    # )
    #   (select book.id from book join publisher on book.id_publisher = publisher.id where publisher.name = '')
    result = session.query(Publisher).filter(or_(Publisher.name == publ_name, Publisher.id == publ_id)).all()
    if len(result) == 0:
        print(f'Не найден издатель по значению наименования или идентификатора \"{publ_name}\"')
        return
    elif len(result) == 1:
        publ_id = result[0].id
        print(f'Поиск магазинов, где продаются книги издательства \"{result[0].name}\":')

    # publisher_books = session.query(Book.id).join(Publisher).filter(or_(Publisher.name == publ_name, Publisher.id == publ_id)).subquery()
    publisher_books = session.query(Book.id).filter(Book.id_publisher == publ_id)
    shops_with_not_zero_stocks = session.query(Stock.id_shop).filter(Stock.id_book.in_(publisher_books)).group_by(
        Stock.id_shop).having(func.sum(Stock.count) > 0).subquery()
    shops = session.query(Shop).filter(Shop.id.in_(shops_with_not_zero_stocks)).all()
    if len(shops) == 0:
        print('магазины не найдены')
        return
    for shop in shops:
        print(shop.name)

    session.close()


def main():
    engine = create_engine('postgresql://Pushkin:1@localhost/BookStore')
    Session = sessionmaker(bind=engine)
    session = Session()
    publ_name = input('Введите наименование или идентификатор издателя: ').strip()
    find_shops_by_publisher(Session(), publ_name)

if __name__ == '__main__':
    main()