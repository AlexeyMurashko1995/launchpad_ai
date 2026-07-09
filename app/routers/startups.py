from fastapi import APIRouter, BackgroundTasks, HTTPException, status, Depends
from app.models.startup import StartupCreate, StartupPublic, StartupUpdate
from app.core.database import delete_startup, get_startup_by_id, update_startup, get_all_startups, create_startup, get_db, AsyncSession
from app.services.ai import generate_mock_analysis

router = APIRouter(prefix='/startups', tags=['Startups'])

@router.get('/', response_model=list[StartupPublic])
async def get_startups(session: AsyncSession = Depends(get_db)):
    all_startups = get_all_startups(session=session)
    return await all_startups


@router.post('/')
async def add_new_startup(startup_data: StartupCreate, background_tasks: BackgroundTasks, session: AsyncSession = Depends(get_db)):
    new_startup = await create_startup(name=startup_data.name, category=startup_data.category, session=session)
    background_tasks.add_task(generate_mock_analysis, new_startup.id)
    return new_startup


@router.get('/{startup_id}', response_model=StartupPublic)
async def get_target_startup(startup_id: int, session: AsyncSession = Depends(get_db)):
    target_startup = await get_startup_by_id(startup_id, session=session)
    if not target_startup:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail='Startup not found')
    return target_startup


@router.delete('/{startup_id}')
async def remove_startup(startup_id: int, session: AsyncSession = Depends(get_db)):
    deleted_startup = await delete_startup(startup_id, session=session)
    if not deleted_startup:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail='Startup not found')
    return {'message': f'startup #{startup_id} was successfully deleted'}


@router.patch('/{startup_id}')
async def modify_startup(startup_id: int, startup_data: StartupUpdate, session: AsyncSession = Depends(get_db)):
    updated_startup = await update_startup(startup_id, startup_data, session=session)
    if not updated_startup:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail='Startup not found')
    return {'status': 'updated'}