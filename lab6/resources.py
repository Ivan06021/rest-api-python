from flask_restful import Resource, reqparse
from flask import jsonify, request
from marshmallow import ValidationError
from models import db, Book
from schemas import BookSchema


book_schema = BookSchema()

class BookListResource(Resource):
    def get(self):
        """
        Get list of books with cursor pagination
        ---
        tags:
          - Books
        parameters:
          - in: query
            name: cursor
            type: integer
            required: false
            description: ID of the last received book
          - in: query
            name: limit
            type: integer
            default: 10
            maximum: 100
            required: false
            description: Number of books to return
        responses:
          200:
            description: List of books
            schema:
              type: object
              properties:
                data:
                  type: array
                  items:
                    $ref: '#/definitions/Book'
                pagination:
                  type: object
                  properties:
                    next_cursor:
                      type: integer
                    has_more:
                      type: boolean
        """
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('cursor', type=int, location='args')
            parser.add_argument('limit', type=int, default=10, location='args')
            args = parser.parse_args()

            limit = min(max(args['limit'], 1), 100)
            query = Book.query.order_by(Book.id)

            if args['cursor']:
                query = query.filter(Book.id > args['cursor'])

            books = query.limit(limit).all()
            next_cursor = books[-1].id if books else None

            response = {
                "data": [book.to_dict() for book in books],
                "pagination": {
                    "next_cursor": next_cursor,
                    "has_more": next_cursor is not None
                }
            }
            return jsonify(response)

        except Exception as e:
            return {"error": str(e)}, 400

    def post(self):
        """
        Create a new book
        ---
        tags:
          - Books
        parameters:
          - in: body
            name: body
            required: true
            schema:
              $ref: '#/definitions/BookInput'
        responses:
          201:
            description: Created book
            schema:
              $ref: '#/definitions/Book'
          400:
            description: Validation error
        """
        try:
            data = book_schema.load(request.get_json())
            book = Book(
                title=data['title'],
                author=data['author'],
                year=data['year']
            )
            db.session.add(book)
            db.session.commit()
            return jsonify(book.to_dict()), 201
        except ValidationError as err:
            return {"error": "Validation error", "details": err.messages}, 400


class BookResource(Resource):
    def get(self, book_id):
        """
        Get book by ID
        ---
        tags:
          - Books
        parameters:
          - in: path
            name: book_id
            type: integer
            required: true
        responses:
          200:
            description: Book details
            schema:
              $ref: '#/definitions/Book'
          404:
            description: Book not found
        """
        book = Book.query.get_or_404(book_id)
        return jsonify(book.to_dict())

    def delete(self, book_id):
        """
        Delete book by ID
        ---
        tags:
          - Books
        parameters:
          - in: path
            name: book_id
            type: integer
            required: true
        responses:
          200:
            description: Book deleted successfully
          404:
            description: Book not found
        """
        book = Book.query.get_or_404(book_id)
        db.session.delete(book)
        db.session.commit()
        return {"message": f"Book with ID {book_id} deleted successfully"}, 200