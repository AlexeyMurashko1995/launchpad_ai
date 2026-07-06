from fastapi import APIRouter, BackgroundTasks, HTTPException, status
from app.core.database import get_all_startups
from app.core.database import create_startup
from app.models.startup import StartupCreate
from app.core.database import delete_startup
from app.core.database import get_startup_by_id
from app.models.startup import StartupPublic

router = APIRouter(prefix='/startups', tags=['Startups'])

@router.get('/', response_model=list[StartupPublic])
async def get_startups():
    return await get_all_startups()


@router.post('/')
async def add_new_startup(startup_data: StartupCreate, background_tasks: BackgroundTasks):
    return await create_startup(name=startup_data.name, category=startup_data.category, background_tasks=background_tasks)


@router.get('/{startup_id}', response_model=StartupPublic)
async def get_target_startup(startup_id: int):
    target_startup = await get_startup_by_id(startup_id)
    if not target_startup:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail='Startup not found')
    return target_startup


@router.delete('/{startup_id}')
async def remove_startup(startup_id: int):
    deleted_startup = await delete_startup(startup_id)
    if not deleted_startup:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail='Startup not found')
    return {'message': f'startup #{startup_id} was successfully deleted'}