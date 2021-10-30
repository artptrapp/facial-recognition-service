from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from ..lib.blo.compare_user_image_blo import compare_user_image

router = APIRouter()

@router.post('/user/{username}/picture-comparison', tags=['picture-comparison'])
async def get_picture_comparison(username: str, image: UploadFile = File(...)):
    comparison_result = await compare_user_image(username, image)
    return JSONResponse(comparison_result)
