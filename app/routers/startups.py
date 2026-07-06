from fastapi import APIRouter, BackgroundTasks
from app.core.database import get_all_startups
from app.core.database import create_startup
from app.models.startup import StartupCreate
from app.core.database import get_startup_by_id

router = APIRouter(prefix='/startups', tags=['Startups'])

@router.get('/')
async def get_startups():
    return await get_all_startups()


@router.post('/')
async def add_new_startup(startup_data: StartupCreate, background_tasks: BackgroundTasks):
    return await create_startup(name=startup_data.name, category=startup_data.category, background_tasks=background_tasks)


@router.get('/{startup_id}')
async def get_target_startup(startup_id: int):
    return await get_startup_by_id(startup_id)