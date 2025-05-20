from marshmallow import Schema, fields


class BookSchema(Schema):
    
    class Meta:
        strict = True
    
    id = fields.Integer(dump_only=True)
    title = fields.String(
        required=True,
        validate=lambda x: 3 <= len(x) <= 30,
        error_messages={
            "required": "Назва книги обов'язкова",
            "validator_failed": "Довжина назви має бути від 3 до 30 символів",
        },
    )
    author = fields.String(
        required=True,
        validate=lambda x: 3 <= len(x) <= 30,
        error_messages={
            "required": "Автор книги обов'язковий",
            "validator_failed": "Довжина імені автора має бути від 3 до 30 символів",
        },
    )
    year = fields.Integer(
        required=True,
        validate=lambda x: 1000 <= x <= 2025,
        error_messages={
            "required": "Рік видання обов'язковий",
            "validator_failed": "Рік має бути між 1000 та 2025",
        },
    )
