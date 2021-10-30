from starlette.responses import JSONResponse
from urllib.parse import urlparse
from app.core.lib.repositories.auth_session_repository import create_auth_session, get_session_by_id
import jwt

jwt_secret = "some_jwt_secret"

async def get_validation_response(token: str, returnUrl: str):
    if not returnUrl:
        return JSONResponse(
            status_code=400,
            content='Missing returnUrl as a parameter'
        )

    if not validate_url(returnUrl):
        return JSONResponse(
            status_code=422,
            content='Return URL is invalid. It must be a valid URL.'
        )

    if not token:
        return JSONResponse(
            status_code=400,
            content='Missing request token. Must be a correctly signed JWT token'
        )

    try:
        decoded_token = decode_token(token)
    except Exception as e:
        print(e)
        return JSONResponse(
            status_code=422,
            content='Invalid JWT token provided.'
        )

    return None


def decode_token(encoded: str):
    return jwt.decode(encoded, jwt_secret, algorithms=['HS256'])


def encode_payload(object: any):
    return jwt.encode(object, jwt_secret)


def validate_url(x):
    try:
        result = urlparse(x)
        return all([result.scheme, result.netloc])
    except:
        return False


async def create_session(user_id: str, return_url: str):
    return await create_auth_session(return_url, user_id)


async def get_session(session_id: str):
    return await get_session_by_id(session_id)