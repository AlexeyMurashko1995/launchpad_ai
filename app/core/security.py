from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
import jwt
from jwt.exceptions import PyJWTError
from sqlmodel import SQLModel, select
from app.models.user import User
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = 'my_secret_key'

ALGORITHM = 'HS256'

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def create_access_token(data: dict, expires_delta: timedelta | None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = expires_delta + datetime.now(timezone.utc)
    else:
        expire = timedelta(minutes=15) + datetime.now(timezone.utc)
    to_encode.update({'exp': expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token


def get_password_hash(password: str) -> str:
    hash_password = pwd_context.hash(password)
    return hash_password


def verify_password(plain_password: str, hash_password: str):
    return pwd_context.verify(plain_password, hash_password)


async def get_current_user(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise HTTPException(status_code=401, detail='Could not validate credentials')
        query = select(User).where(User.username==username)
        result = await session.execute(query)
        user = result.scalar_one_or_none()
        if user is None:
            raise HTTPException(status_code=401, detail='Could not validate credentials')
        return user
    except PyJWTError:
        raise HTTPException(status_code=401, detail='Could not validate credentials')


