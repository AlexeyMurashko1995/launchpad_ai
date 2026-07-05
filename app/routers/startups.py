from fastapi import APIRouter
from app.core.database import get_all_startups

router = APIRouter(prefix='/startups', tags=['Startups'])

@router.get('/')
async def get_startups():
    return await get_all_startups()