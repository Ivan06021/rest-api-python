from flask import Flask
from models import db, Book
from flask_restful import Api
from flasgger import Swagger
from resources import BookListResource, BookResource


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "postgresql://postgres:postgres@db/library_db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    app.config['SWAGGER'] = {
        'title': 'Library API',
        'uiversion': 3,
        'specs_route': '/api/docs/'
    }

    db.init_app(app)
    
    api = Api(app)
    api.add_resource(BookListResource, '/api/v1/books')
    api.add_resource(BookResource, '/api/v1/books/<int:book_id>')
    
    swagger = Swagger(app, template={
        "swagger": "2.0",
        "info": {
            "title": "Library API",
            "description": "API for managing library books",
            "version": "1.0"
        },
        "definitions": {
            "Book": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "title": {"type": "string"},
                    "author": {"type": "string"},
                    "year": {"type": "integer"}
                }
            },
            "BookInput": {
                "type": "object",
                "required": ["title", "author", "year"],
                "properties": {
                    "title": {"type": "string", "minLength": 3, "maxLength": 30},
                    "author": {"type": "string", "minLength": 3, "maxLength": 30},
                    "year": {"type": "integer", "minimum": 1000, "maximum": 2025}
                }
            }
        }
    })

    with app.app_context():
        db.create_all()
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
