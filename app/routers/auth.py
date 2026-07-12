from fastapi import APIRouter
from app.models.user import User, UserCreate

router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post('/register')
async def register_user(user_data: UserCreate):
    return {'status': 'ok'}