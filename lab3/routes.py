from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from schemas import BookSchema
from models import db, Book, get_all_books, get_book_by_id, add_book, delete_book

books_bp = Blueprint("books", __name__, url_prefix="/api/v1")

book_schema = BookSchema()


@books_bp.route("/books", methods=["GET"])
def get_all_books_endpoint():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    books = get_all_books(page=page, per_page=per_page)
    return jsonify(books), 200


@books_bp.route("/books/<int:book_id>", methods=["GET"])
def get_book_by_id_endpoint(book_id):
    book = get_book_by_id(book_id)

    if book:
        return jsonify(book), 200
    else:
        return jsonify({"error": f"Книга з ID {book_id} не знайдена"}), 404


@books_bp.route("/books", methods=["POST"])
def add_book_endpoint():
    try:
        book_data = book_schema.load(request.json)
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400

    new_book = add_book(book_data)
    return jsonify(new_book), 201


@books_bp.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book_endpoint(book_id):
    if delete_book(book_id):
        return jsonify({"message": "Книга видалена"}), 200
    else:
        return jsonify({"error": f"Книга з ID {book_id} не знайдена"}), 404


def register_routes(app):
    app.register_blueprint(books_bp)
