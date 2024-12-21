from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel, Field


app=FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    publish_date: int

    def __init__(self, id: int, title: str, author: str, description: str, rating: int, publish_date: int):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.publish_date = publish_date

class BookRequest(BaseModel):
    id: Optional[int]= Field(description='ID is not needed on create', default=None) 
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=6)
    publish_date: int = Field(gt=2000, lt=2030)

    model_config = {
        "json_schema_extra":{
            "example":{
                "title": "A new book",
                "author": "Coding with Dren",
                "description": "This is a description for that book",
                "rating": 5,
                "publish_date": 2022
            }
        }
    }


BOOKS=[
    Book(1, 'Book 1', 'Author 1', 'Description 1', 5, 2020),
    Book(2, 'Book 2', 'Author 2', 'Description 2', 4, 2020),
    Book(3, 'Book 3', 'Author 3', 'Description 3', 3, 2019),
    Book(4, 'Book 4', 'Author 4', 'Description 4', 2, 2018),
    Book(5, 'Book 5', 'Author 5', 'Description 5', 1, 2021)

]

@app.get('/books')
async def read_all_books():
    return BOOKS


#READ BOOK BY ID
@app.get("/books/{book_id}")
async def read_book_by_id(book_id: int):
    for book in BOOKS:
        if book.id == book_id:
            return book

#FETCH BOOKS BY RATING
@app.get("/books/")
async def read_books_by_rating(book_rating: int):
    # return [book for book in BOOKS if book.rating == rating]
    books_to_return=[]
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return

#READ BOOKS BY PUBLISHED YEAR
@app.get("/books/publish/")
async def read_books_by_publish_date(publish_date: int):
    books_to_return=[]
    for book in BOOKS:
        if book.publish_date==publish_date:
            books_to_return.append(book)
    return books_to_return


#CREATE BOOK
@app.post("/create-book")
async def create_book(book_request: BookRequest):
    new_book=Book(**book_request.model_dump())
    print(type(new_book))
    BOOKS.append(find_book_id(new_book))
    

def find_book_id(book: Book):
    book.id=1 if len(BOOKS)==0 else BOOKS[-1].id+1
    return book

#UPDATE BOOK BY ID

@app.put("/books/update_book")
async def update_book(book: BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i]=book

#DELETE BOOK BY ID
@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            break