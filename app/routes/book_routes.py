from fastapi import APIRouter, Depends, HTTPException
from dependencies import cath_session
from models import Book
from main import bcrypt_context
from schemas import BookSchema
from sqlalchemy.orm import Session
from services.google_api import search_books_service , get_book_by_id 

book_router = APIRouter(prefix = "/books", tags = ["books"])


@book_router.get("/search_books")
def search_books(title:str):
      book = search_books_service(title)
      return book

@book_router.post("/add_books")
def save_book(book_schema: BookSchema, session: Session = Depends(cath_session)):
    data = get_book_by_id(book_schema.google_books_id)
    info = data["volumeInfo"]

    isbn = None
    for identifier in info.get("industryIdentifiers", []):
        if identifier["type"] == "ISBN_13":
            isbn = identifier["identifier"]
            break

    new_book = Book(
        title=info.get("title"),
        categories=", ".join(info.get("categories", [])),
        average_rating=info.get("averageRating", 0.0),
        rating_count=info.get("ratingsCount", 0),
        my_rating=book_schema.my_rating,
        status=book_schema.status,
        isbn=isbn,
      #   user_id=current_user.id
    )

    session.add(new_book)
    session.commit()
    session.refresh(new_book)
    return new_book

@book_router.get("/count_books")
def book_count(session: Session = Depends(cath_session)):
    counts = {
        "to_read": session.query(Book).filter(Book.status == "to_read").count(),
        "reading": session.query(Book).filter(Book.status == "reading").count(),
        "finished": session.query(Book).filter(Book.status == "finished").count(),
    }
    return counts
