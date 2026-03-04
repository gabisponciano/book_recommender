from fastapi import FastAPI
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

load_dotenv

SECRET_KEY = os.getenv("SECRET_KEY")

app = FastAPI()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

from routes.auth_routes import auth_router
from routes.book_routes import book_router

app.include_router(auth_router)
app.include_router(book_router)
# @app.get("/")
# async def root():  
#     return {"message": "Hello World"}