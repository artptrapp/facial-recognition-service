from fastapi import APIRouter

router = APIRouter()

@router.get('/', tags=['root'])
async def root_request():
    return {
        'ok': True
    }
