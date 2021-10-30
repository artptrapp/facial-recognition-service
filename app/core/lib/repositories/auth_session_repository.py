from app.core.lib.utils.mongo_client import MongoWrapper
import uuid


def create_unique_session_token():
    return uuid.uuid4().hex


async def create_auth_session(return_url: str, user_id: str):
    session_collection = MongoWrapper().get_collection('auth_session')
    session_object = {
        'return_url': return_url,
        'user_id': str(user_id),
        'session_id': create_unique_session_token()
    }
    session_collection.insert_one(session_object)
    return session_object


async def get_session_by_id(session_id: str):
    session_collection = MongoWrapper().get_collection('auth_session')
    return session_collection.find_one({'session_id': session_id})
