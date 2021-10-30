from app.core.lib.utils.mongo_client import MongoWrapper
from fastapi.datastructures import UploadFile
from app.core.lib.image_processing.compare_images import get_image_encoding
from datetime import datetime

import pickle

async def get_by_id(id: int):
    user = None
    for element in mock_users_database:
        if element['id'] == id:
            user = element
            break
    return user


async def get_by_name(name: str):
    users_collection = MongoWrapper().get_collection('users')
    return users_collection.find_one({'name': name})


async def create(name: str):
    users_collection = MongoWrapper().get_collection('users')
    user_object = {
        'name': name,
        'created_at': datetime.now()
    }
    users_collection.insert_one(user_object)

    return user_object


async def create_seed(username: str, image: UploadFile):
    user = await get_by_name(username)
    if user is None:
        user = await create(username)

    encoding = await get_image_encoding(image)
    users_collection = MongoWrapper().get_collection('users')
    users_collection.update_one(
        {
            'name': username
        },
        {
            '$push': {
                'known_faces': pickle.dumps(encoding)
            }
        })

    return True
