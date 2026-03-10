import requests
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")
url = "https://www.googleapis.com/books/v1/volumes"

def search_books_service(title: str):

    response = requests.get(
        url,
        params={"q": title, "key": API_KEY}
    )

    return response.json()


def get_book_by_id(google_books_id: str) -> dict:
    url = f"https://www.googleapis.com/books/v1/volumes/{google_books_id}"
    response = requests.get(
        url,
        params={"key": API_KEY} 
                            
      )
    response.raise_for_status()
    return response.json()

