from flask import request, jsonify, Blueprint
from marshmallow import ValidationError

from schemas import BookSchema
import models

books_bp = Blueprint("books", __name__, url_prefix="/api/v1")

book_schema = BookSchema()


@books_bp.route("/books", methods=["GET"])
def get_all_books():
    return jsonify(models.get_all_books()), 200


@books_bp.route("/books/<int:book_id>", methods=["GET"])
def get_book_by_id(book_id):
    book = models.get_book_by_id(book_id)

    if book:
        return jsonify(book), 200
    else:
        return jsonify({"error": f"Книга з ID {book_id} не знайдена"}), 404


@books_bp.route("/books", methods=["POST"])
def add_book():
    json_data = request.get_json()

    if not json_data:
        return jsonify({"error": "Дані не надійшли"}), 400

    try:
        data = book_schema.load(json_data)

        new_book = models.add_book(data)

        return jsonify(new_book), 201

    except ValidationError as err:
        return jsonify({"error": "Помилка валідації", "details": err.messages}), 400


@books_bp.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    result = models.delete_book(book_id)

    if result:
        return jsonify({"message": f"Книга з ID {book_id} видалена успішно"}), 200
    else:
        return jsonify({"error": f"Книга з ID {book_id} не знайдена"}), 404


def register_routes(app):
    app.register_blueprint(books_bp)
