from fastapi import APIRouter, Depends, HTTPException
from models import User, db
from dependencies import cath_session
from main import bcrypt_context
from schemas import UserSchema
from sqlalchemy.orm import Session

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/home")
async def authenticate():
      return {"Auntenticação"}


@auth_router.post("/create_account")
async def crate_account(user_schema:UserSchema, session: Session = Depends(cath_session)):
      user = session.query(User).filter(User.email==user_schema.email).first()
      if user:
            raise HTTPException(status_code=400, detail="User already exists!")
      else: 
            crypto_pwrd = bcrypt_context.hash(user_schema.pwrd)
            new_user = User(user_schema.name, user_schema.email, crypto_pwrd, user_schema.active, user_schema.admin)
            session.add(new_user)
            session.commit()
            return {f"Message: User created! {user_schema.email}"}