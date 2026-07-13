from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.models.user import User, UserCreate, UserPublic
from app.core.database import get_db
from app.core.security import get_password_hash, verify_password, create_access_token, get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

router = APIRouter(prefix='/auth', tags=['Auth'])


@router.get('/me', response_model=UserPublic)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post('/register', response_model=UserPublic)
async def register_user(user_data: UserCreate, session: AsyncSession = Depends(get_db)):
    query = select(User).where(user_data.username == User.username)
    result = await session.execute(query)
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=400, detail='Username already taken')
    hashed_password = get_password_hash(user_data.password)
    new_user = User(username=user_data.username, hashed_password=hashed_password)
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


@router.post('/login')
async def login_user(user_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_db)):
    query = select(User).where(user_data.username==User.username)
    result = await session.execute(query)
    bd_user = result.scalar_one_or_none()
    if not bd_user:
        raise HTTPException(status_code=401, detail='Login or password are incorrect')
    comparison = verify_password(user_data.password, bd_user.hashed_password)
    if not comparison:
        raise HTTPException(status_code=401, detail='Login or password are incorrect')
    access_token = create_access_token(data={'sub': bd_user.username})
    return {'access_token': access_token, 'token_type': 'bearer'}

