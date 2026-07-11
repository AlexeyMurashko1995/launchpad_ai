from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
import jwt
from jwt.exceptions import PyJWTError
from sqlmodel import SQLModel, select
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = 'my_secret_key'
ALGORITHM = 'HS256'

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