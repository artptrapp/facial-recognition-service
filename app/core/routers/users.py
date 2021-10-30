from app.core.lib.repositories.user_repository import create_seed
from app.core.lib.models.entities.User import User
from app.core.lib.blo import user_blo
from fastapi import APIRouter, Request, File, UploadFile
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post('/user/', tags=['create-user'])
async def create_user(request: Request):
    body = await request.json()
    creation_result = await user_blo.create_user(body)
    return JSONResponse(creation_result)

@router.post('/user/{username}/seeds', tags=['add-seed'])
async def create_seed_for_user(username: str, image: UploadFile = File(...)):
    await create_seed(username, image)
    return True