from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import BaseModel

from sqlmodel import select
from models.users import Users
from database import SessionDep

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None

class UserResponse(BaseModel):
    id: int
    username: str
    password: str

    class Config:
        orm_mode = True

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user(username: str, session: SessionDep) -> Users | None:
    user = session.exec(select(Users).where(Users.username == username)).first()
    return user

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(username: str, password: str, session: SessionDep) -> Users| bool:
    user = get_user(username, session)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def add_user(username: str, password: str, session: SessionDep):
    hashed_password = get_password_hash(password)
    session.add(Users(username=username, password=hashed_password))
    session.commit()
    return

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        token_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

    if token_data:
        return True
    
    else:
        raise HTTPException(status_code=401, detail="Not authenticated")

@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep
) -> Token:
    user = authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.post("/users/add/")
async def add_users(
    form_data: Users, session: SessionDep, current_user: Users = Depends(get_current_user)
):  
    if not form_data.username or not form_data.password:
        raise HTTPException(status_code=400, detail="Необходимо указать имя пользователя и пароль")

    add_user(form_data.username, form_data.password, session)

    return {"status": "Пользователь добавлен", "username": form_data.username}


@router.get("/users/{user_id}")
async def read_users(user_id: int, session: SessionDep, current_user: Users = Depends(get_current_user)):
    user = session.get(Users, user_id)

    if user is None:

        raise HTTPException(status_code=401, detail="Пользователь не найден")
            
    return {"username": user.username}

@router.delete("/users/{user_id}")
async def delete_user(user_id: int, session: SessionDep, current_user: Users = Depends(get_current_user)):
    user = session.get(Users, user_id)
    
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
       
    session.delete(user)

    session.commit()
    return {"status": f"Пользователь удален", "user_id": user_id}

@router.put("/users/{user_id}")
async def update_user(user_id: int, new_password: str, session: SessionDep, current_user: Users = Depends(get_current_user)):
    user = session.get(Users, user_id)
    
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
       
    user.password = get_password_hash(new_password)

    session.add(user)

    session.commit()

    return {"status": f"Пароль пользователя обновлен", "user_id": user_id}















