from fastapi import APIRouter

router = APIRouter(prefix='/startups', tags=['Startups'])

@router.get('/')
async def get_startups():
    return {'message': 'success'}