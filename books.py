from fastapi import FastAPI, Body

app = FastAPI()

BOOKS = [
    {'title': 'title one', 'author': 'Author 1', 'category': 'category1'},
    {'title': 'title 2', 'author': 'Author 2', 'category': 'category2'},
    {'title': 'title 3', 'author': 'Author 3', 'category': 'category3'},
    {'title': 'title 4', 'author': 'Author 4', 'category': 'category4'},
    {'title': 'title 5', 'author': 'Author 5', 'category': 'category5'},
    {'title': 'title 6', 'author': 'Author 6', 'category': 'category6'},
]


@app.get("/")
async def first_api():
    return {"message": "Hello Eric"}


@app.get("/api-endpoint")
async def first_api():
    return {"message": "Hello Mohit"}


@app.get("/books")
async def all_books():
    return BOOKS


@app.get("/books/{book_title}")
async def read_book(book_title: str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book


@app.get("/books/")
async def read_category_by_query(category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            books_to_return.append(book)

    return books_to_return


@app.get("/books/{book_author}/")
async def read_author_category_by_query(book_author: str, category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == book_author.casefold() and book.get('category').casefold() == category.casefold():
            books_to_return.append(book)

    return books_to_return


@app.post("/books/create_book")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)


@app.put("/book/update_book")
async def update_book(updated_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == updated_book.get('title').casefold():
            BOOKS[i] = updated_book


@app.delete("/book/delete_book/{book_title}")
async def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            BOOKS.pop(i)
            break
