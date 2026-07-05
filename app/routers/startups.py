from fastapi import APIRouter, BackgroundTasks
from app.core.database import get_all_startups
from app.core.database import create_startup

router = APIRouter(prefix='/startups', tags=['Startups'])

@router.get('/')
async def get_startups():
    return await get_all_startups()


@router.post('/')
async def add_new_startup(name: str, category: str, background_tasks: BackgroundTasks):
    return await create_startup(name=name, category=category, background_tasks=background_tasks)