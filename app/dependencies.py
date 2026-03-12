from models import User, db
from sqlalchemy.orm import sessionmaker, Session
from models import User
from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from main import ALGORITHM, SECRET_KEY, outh2_schema

def cath_session():
      try:
            Session = sessionmaker(bind = db)
            session = Session()
            yield session
      finally:
            session.close()

def verify_token(token: str = Depends(outh2_schema), session: Session = Depends(cath_session)):
      try:
            dic_info = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id = int(dic_info.get("sub"))
      except JWTError as error:
            raise HTTPException(status_code=401, detail="Access Denied")
      user = session.query(User).filter(User.id==user_id).first()
      if not user:
            raise HTTPException(status_code=401, detail="Invalid Access")
      
      return user
      

