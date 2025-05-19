from flask_sqlalchemy import SQLAlchemy
from typing import List, Dict, Tuple

db = SQLAlchemy()


class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    author = db.Column(db.String(30), nullable=False)
    year = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
        }


def get_all_books(cursor: int = None, limit: int = 10) -> Tuple[List[Dict], int]:
    query = Book.query.order_by(Book.id)

    if cursor:
        query = query.filter(Book.id > cursor)

    books = query.limit(limit).all()
    next_cursor = books[-1].id if books else None

    return [book.to_dict() for book in books], next_cursor


def get_book_by_id(book_id: int) -> Dict or None:
    book = Book.query.get(book_id)
    return book.to_dict() if book else None


def add_book(book_data: Dict) -> Dict:
    book = Book(
        title=book_data["title"], author=book_data["author"], year=book_data["year"]
    )
    db.session.add(book)
    db.session.commit()
    return book.to_dict()


def delete_book(book_id: int) -> bool:
    book = Book.query.get(book_id)
    if book:
        db.session.delete(book)
        db.session.commit()
        return True
    return False
