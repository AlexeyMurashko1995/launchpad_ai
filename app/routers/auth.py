from fastapi import APIRouter, Depends, HTTPException
from app.models.user import User, UserCreate
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post('/register')
async def register_user(user_data: UserCreate, session: AsyncSession = Depends(get_db)):
    query = select(User).where(user_data.username == User.username)
    result = await session.execute(query)
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=400, detail='Username already taken')

