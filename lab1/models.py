from typing import List, Dict

books_db: List[Dict] = [
    {"id": 1, "title": "Кобзар", "author": "Тарас Шевченко", "year": 1840},
    {"id": 2, "title": "Лісова пісня", "author": "Леся Українка", "year": 1911},
    {"id": 3, "title": "Тигролови", "author": "Іван Багряний", "year": 1944},
]


def get_all_books() -> List[Dict]:
    return books_db


def get_book_by_id(book_id: int) -> Dict or None:
    return next((book for book in books_db if book["id"] == book_id), None)


def add_book(book_data: Dict) -> Dict:
    new_id = max(book["id"] for book in books_db) + 1 if books_db else 1

    new_book = {
        "id": new_id,
        "title": book_data["title"],
        "author": book_data["author"],
        "year": book_data["year"],
    }

    books_db.append(new_book)

    return new_book


def delete_book(book_id: int) -> bool:
    global books_db
    book = get_book_by_id(book_id)

    if book:
        books_db = [book for book in books_db if book["id"] != book_id]
        return True
    return False
