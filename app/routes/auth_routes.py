from fastapi import APIRouter, Depends, HTTPException
from models import User, db
from dependencies import cath_session, verify_token
from main import bcrypt_context, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from schemas import UserSchema, LoginSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime,timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm


auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/home")
async def authenticate():
      return {"Message"}

      

def create_token(id_user, token_time = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
      expirate_date = datetime.now(timezone.utc) + token_time
      dic_info = {"sub": str(id_user), "exp":expirate_date}
      jwt_cod = jwt.encode(dic_info, SECRET_KEY, ALGORITHM)
      return jwt_cod


def user_authenticate(email, pwrd, session):
      user = session.query(User).filter(User.email==email).first()
      if not user:
            return False
      elif not bcrypt_context.verify(pwrd, user.pwrd):
            return False
      return user

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

@auth_router.post("/login")
async def login(login_schema:LoginSchema, session: Session = Depends(cath_session)):
      user = user_authenticate(login_schema.email, login_schema.pwrd, session)
      if not user:
            raise HTTPException(status_code=400, detail="User not found or invalid credentials")
      else:
            access_token = create_token(user.id)
            refresh_token = create_token(user.id, timedelta(days=7))
            return {
                  "access_token": access_token,
                  "refresh_token": refresh_token,
                  "token_type": "Bearer"
            } 
      
@auth_router.post("/login-form")
async def login_form(data_form: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(cath_session)):
      user = user_authenticate(data_form.username, data_form.password, session)
      if not user:
            raise HTTPException(status_code=400, detail="User not found or invalid credentials")
      else:
            access_token = create_token(user.id)
            return {
                  "access_token": access_token,
                  "token_type": "Bearer"
            } 

@auth_router.post("/refresh")
async def use_refresh_token(user: User = Depends(verify_token)):
      access_token = create_token(user.id)
      return {
                  "access_token": access_token,
                  "token_type": "Bearer"
            }