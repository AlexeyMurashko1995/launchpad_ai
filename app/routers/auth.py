from fastapi import APIRouter, Depends, HTTPException
from app.models.user import User, UserCreate, UserPublic
from app.core.database import get_db
from app.core.security import get_password_hash, verify_password
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

router = APIRouter(prefix='/auth', tags=['Auth'])


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

