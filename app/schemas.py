from pydantic import BaseModel
from typing import Optional
from enum import Enum

class UserSchema(BaseModel):
      name: str
      email: str
      pwrd: str
      active: Optional[bool]
      admin: Optional[bool]

      class Config:
            from_attributes = True

class LoginSchema(BaseModel):
      email: str
      pwrd: str

      class Config:
            from_attributes = True

class BookStatus(str, Enum):
    to_read = "to_read"
    reading = "reading"
    finished = "finished"

class BookSchema(BaseModel):
      google_books_id: str
      status: BookStatus   # to_read, reading, finished
      my_rating: Optional[int] = None

      class Config:
            from_attributes = True