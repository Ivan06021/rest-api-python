from fastapi import APIRouter, HTTPException, status
from models import get_all_books, get_book_by_id, add_book, delete_book
from schemas import BookSchema
from typing import List


router = APIRouter(tags=["books"])


@router.get("/books", response_model=List[BookSchema])
async def get_all_books_endpoint():
    return await get_all_books()


@router.get("/books/{book_id}", response_model=BookSchema)
async def get_book_by_id_endpoint(book_id: int):
    book = await get_book_by_id(book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Книга з ID {book_id} не знайдена",
        )
    return book


@router.post("/books", response_model=BookSchema, status_code=status.HTTP_201_CREATED)
async def add_book_endpoint(book: BookSchema):
    try:
        return await add_book(book)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/books/{book_id}")
async def delete_book_endpoint(book_id: int):
    result = await delete_book(book_id)
    if result:
        return {"message": f"Книга з ID {book_id} видалена успішно"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Книга з ID {book_id} не знайдена",
    )
