from fastapi import APIRouter, Depends
from app.models.user import User, UserCreate
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post('/register')
async def register_user(user_data: UserCreate, session: AsyncSession = Depends(get_db)):
    return {'status': 'ok'}