from app.core.lib.models.errors.user_already_exists_error import UserAlreadyExistsError
from app.core.lib.utils.mongo_client import MongoWrapper
from app.core.lib.models.errors.no_face_found_error import NoFaceFoundError
from starlette.requests import Request
from app.core.lib.models.errors.user_not_found_error import UserNotFoundError
from app.core.lib.models.errors.invalid_image_error import InvalidImageError
from app.core.lib.models.errors.no_face_found_error import NoFaceFoundError
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.config import settings
from .core.routers import root, picture_comparison, users, html_pages

import os
import shutil

def get_application():
    _app = FastAPI(title=settings.PROJECT_NAME)
    print(settings.BACKEND_CORS_ORIGINS)
    _app.add_middleware(
        CORSMiddleware,
        #allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    _app.include_router(root.router)
    _app.include_router(picture_comparison.router)
    _app.include_router(users.router)
    _app.include_router(html_pages.router)

    print('-- Deleting temp folder contents --')
    with os.scandir('app/temp/') as entries:
        for entry in entries:
            if entry.is_dir() and not entry.is_symlink():
                shutil.rmtree(entry.path)
            else:
                os.remove(entry.path)

    print('-- Temp folder contents deleted successfully --')
    MongoWrapper().initialize()

    return _app


app = get_application()

@app.exception_handler(UserNotFoundError)
async def user_not_found_error_handler(_: Request, exception: UserNotFoundError):
    return JSONResponse(
        status_code=404,
        content=exception.to_json()
    )

@app.exception_handler(InvalidImageError)
async def invalid_image_error_handler(_: Request, exception: InvalidImageError):
    return JSONResponse(
        status_code=422,
        content=exception.to_json()
    )

@app.exception_handler(NoFaceFoundError)
async def no_face_found_error_handler(_: Request, exception: NoFaceFoundError):
    return JSONResponse(
        status_code=400,
        content=exception.to_json()
    )

@app.exception_handler(UserAlreadyExistsError)
async def user_already_exists_error_handler(_: Request, exception: UserAlreadyExistsError):
    return JSONResponse(
        status_code=exception.related_status_code,
        content=exception.to_json()
    )