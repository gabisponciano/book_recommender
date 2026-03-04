from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils.types import ChoiceType
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "database.db")

db = create_engine(f"sqlite:///{os.path.abspath(DB_PATH)}")

base = declarative_base()

class User(base):
      __tablename__ = "users"

      id = Column("id", Integer, primary_key = True, autoincrement=True)
      name = Column("name", String)
      email = Column("email", String, nullable = False)
      pwrd = Column("pwrd", String)
      active = Column("active", Boolean)
      admin = Column("admin", Boolean, default = False)

      def __init__(self, name, email, pwrd, active= True, admin=False):
            self.name = name
            self.email = email
            self.pwrd = pwrd
            self.active = active
            self.admin = admin

class Book(base):
      __tablename__ = "book"

      # BOOK_STATUS = {
      #       ("TO READ", "TO READ"),
      #       ("READING", "READING"),
      #       ("FINISHED", "FINISHED")
      # }

      id = Column("id", Integer, primary_key = True, autoincrement=True)
      title = Column("title", String)
      categories = Column("categories", String)
      average_rating = Column("average_rating", String)
      rating_count = Column("rating_count", Float)
      my_rating = Column("my_rating", Integer, nullable = True)
      status = Column("status", String) ## to_read, reading and finished
      isbn = Column("isbn", String)


      def __init__(self, title, categories, average_rating, rating_count, my_rating, status, isbn):
            self.title = title
            self.categories = categories
            self.average_rating = average_rating 
            self.rating_count = rating_count
            self.my_rating = my_rating
            self.status = status
            self.isbn = isbn


