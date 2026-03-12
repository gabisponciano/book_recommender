from fastapi import APIRouter, Depends, HTTPException
from dependencies import cath_session, verify_token
from models import Book, User
from main import bcrypt_context
from schemas import BookSchema, BookUpdateSchema
from sqlalchemy.orm import Session
from services.google_api import search_books_service , get_book_by_id 


book_router = APIRouter(prefix = "/books", tags = ["books"])

# For userr auth if user.admin = False or/and user.id != book.user

@book_router.get("/search_books")
def search_books(title:str):
      book = search_books_service(title)
      return book


@book_router.get("/my_books")
async def get_books(session: Session = Depends(cath_session), user: User = Depends(verify_token)):
    itens = session.query(Book).all()
    return itens

# user: User = Depends(verify_token)
@book_router.post("/add_books")
def save_book(book_schema: BookSchema, session: Session = Depends(cath_session), user: User = Depends(verify_token)):
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
    )
    new_book.user_id = user.id

    session.add(new_book)
    session.commit()
    session.refresh(new_book)
    return new_book

@book_router.get("/count_books")
def book_count(session: Session = Depends(cath_session), user: User = Depends(verify_token)):
    if Book.user_id == user.id:
        counts = {
            "to_read": session.query(Book).filter(Book.status == "to_read").count(),
            "reading": session.query(Book).filter(Book.status == "reading").count(),
            "finished": session.query(Book).filter(Book.status == "finished").count(),
        }
        return counts

@book_router.post("/edit_book/{book_id}")
async def book_edit(book_schema: BookUpdateSchema, book_id: int, session: Session = Depends(cath_session), user: User = Depends(verify_token)):
    book = session.query(Book).filter(Book.id==book_id).first()
    if not book:
        raise HTTPException(status_code=400, detail="Book not found")
    book.status = book_schema.status
    book.my_rating = book_schema.my_rating
    session.commit()
    session.refresh(book)

    return{
        "message:" f"Book was updated {book.id}"
        "book": book
    }

@book_router.delete("/delete_book/{book_id}")
async def book_delete(book_id: int, session: Session = Depends(cath_session), user: User = Depends(verify_token)):
    book = session.query(Book).filter(Book.id==book_id).first()
    if not book:
        raise HTTPException(status_code=400, detail="Book not found")
    session.delete(book)
    session.commit()
    return{
        "message": f"Book Deleted {book.id}",
        "book": book
    }
    
