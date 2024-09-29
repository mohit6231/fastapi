from fastapi import FastAPI, Body, Path, Query, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from starlette import status

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):
    # id: Optional[int] = None
    id: Optional[int] = Field(
        description='ID is not needed on  create', default=None)
    title: str = Field(min_length=3)
    author: str
    description: str
    rating: int = Field(gt=0, lt=5)
    published_date: int = Field(default=2012)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new book",
                "author": "Tom Danielle",
                "description": "demo content",
                "rating": 4,
                "published_date": 2012
            }
        }
    }


BOOKS = [
    Book(1, 'Book1', 'Author1', 'Book1 Author1', 5, 2012)
]


@app.get("/books", status_code=status.HTTP_200_OK)
async def all_books():
    return BOOKS


@app.post("/books/create-book")
async def create_book(book_request: BookRequest):
    # BOOKS.append(book_request)
    new_book = Book(**book_request.dict())
    # BOOKS.append(new_book)
    BOOKS.append(find_book_id(new_book))


def find_book_id(book: Book):
    # if len(BOOKS) > 0:
    #     book.id = BOOKS[-1].id + 1
    # else:
    #     book.id = 1
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1

    return book


@app.get("/books/{book_id}")
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book

    raise HTTPException(status_code=404, detail='Item Not Found')


@app.get("/books/")
async def read_book(book_rating: int = Query(gt=0, lt=6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)

    return books_to_return


@app.put("/books/update_book")
async def update_book(book: BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_changed = True
            break
    if not book_changed:
        raise HTTPException(status_code=404, detail='Item Not Found')


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_changed = True
            break
    if not book_changed:
        raise HTTPException(status_code=404, detail='Item Not Found')


@app.get("/books/publish")
async def published_date(published_date: int):
    books_to_return = []
    for book in BOOKS:
        if book.published_date == published_date:
            books_to_return.append(book)

    return books_to_return
