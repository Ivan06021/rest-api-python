# main.py
from flask import Flask
from models import db, Book


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "postgresql://postgres:postgres@db/library_db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()
        # Add sample data if the database is empty
        if Book.query.count() == 0:
            sample_books = [
                {"title": "Кобзар", "author": "Тарас Шевченко", "year": 1840},
                {"title": "Лісова пісня", "author": "Леся Українка", "year": 1911},
                {"title": "Тигролови", "author": "Іван Багряний", "year": 1944},
            ]
            for book_data in sample_books:
                book = Book(**book_data)
                db.session.add(book)
            db.session.commit()

    from routes import register_routes

    register_routes(app)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0")
