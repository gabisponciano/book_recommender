from fastapi import APIRouter

book_router = APIRouter(prefix = "/books", tags = ["books"])


@book_router.get("/")
async def list_books():
      return {"Depois vejo a chamada de API"}