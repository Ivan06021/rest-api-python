from motor.motor_asyncio import AsyncIOMotorClient
from schemas import BookSchema
from bson import ObjectId


class Database:
    client: AsyncIOMotorClient = None
    db = None


db = Database()


async def get_database() -> AsyncIOMotorClient:
    return db.client


async def connect_to_mongo():
    db.client = AsyncIOMotorClient("mongodb://mongo_admin:password@mongo:27017")
    db.db = db.client.library
    print("Connected to MongoDB")


async def close_mongo_connection():
    db.client.close()
    print("Closed MongoDB connection")


async def get_all_books():
    books = []
    async for book in db.db.books.find():
        books.append(BookSchema(**book))
    return books


async def get_book_by_id(book_id: str):
    try:
        book = await db.db.books.find_one({"_id": ObjectId(book_id)})
        return BookSchema(**book) if book else None
    except:
        return None


async def add_book(book_data: BookSchema):
    book_dict = book_data.dict(by_alias=True, exclude={"id"})
    result = await db.db.books.insert_one(book_dict)
    new_book = await get_book_by_id(str(result.inserted_id))
    return new_book


async def delete_book(book_id: str):
    try:
        result = await db.db.books.delete_one({"_id": ObjectId(book_id)})
        return result.deleted_count > 0
    except:
        return False
