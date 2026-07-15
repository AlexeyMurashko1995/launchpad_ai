from fastapi import APIRouter, BackgroundTasks, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import (
    delete_startup,
    get_startup_by_id,
    update_startup,
    get_all_startups,
    create_startup,
    get_db,
)
from app.models.startup import Startup, StartupCreate, StartupPublic, StartupUpdate
from app.models.user import User
from app.core.security import get_current_user
from app.services.ai import generate_mock_analysis

router = APIRouter(prefix='/startups', tags=['Startups'])


@router.get('/', response_model=list[StartupPublic])
async def get_startups(session: AsyncSession = Depends(get_db)):
    all_startups = await get_all_startups(session=session)
    return all_startups


@router.post('/', response_model=StartupPublic)
async def add_new_startup(
    startup_data: StartupCreate,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_startup = await create_startup(
        name=startup_data.name,
        category=startup_data.category,
        user_id=current_user.id,
        session=session,
    )
    background_tasks.add_task(generate_mock_analysis, new_startup.id)
    return new_startup


@router.get('/{startup_id}', response_model=StartupPublic)
async def get_target_startup(
    startup_id: int, session: AsyncSession = Depends(get_db)
):
    target_startup = await get_startup_by_id(startup_id, session=session)
    if not target_startup:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Startup not found'
        )
    return target_startup


@router.delete('/{startup_id}')
async def remove_startup(
    startup_id: int,
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    target_startup = await get_startup_by_id(startup_id=startup_id, session=session)
    if not target_startup:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Startup not found')
    if target_startup.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You do not have permission to delete this startup')
    deleted_startup = await delete_startup(startup_id, session=session)
    if not deleted_startup:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Startup not found'
        )
    return {'message': f'startup #{startup_id} was successfully deleted'}


@router.patch('/{startup_id}', response_model=StartupPublic)
async def modify_startup(
    startup_id: int,
    startup_data: StartupUpdate,
    session: AsyncSession = Depends(get_db),
):
    updated_startup = await update_startup(
        startup_id, startup_data, session=session
    )
    if updated_startup is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Startup not found'
        )
    return updated_startup