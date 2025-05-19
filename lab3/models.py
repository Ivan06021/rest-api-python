from flask_sqlalchemy import SQLAlchemy
from typing import List, Dict

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


def get_all_books(page: int = 1, per_page: int = 10) -> List[Dict]:
    return [
        book.to_dict()
        for book in Book.query.paginate(page=page, per_page=per_page).items
    ]


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
