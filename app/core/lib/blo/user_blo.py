from app.core.lib.models.errors.invalid_body_error import InvalidBodyError
from app.core.lib.models.errors.user_already_exists_error import UserAlreadyExistsError
from app.core.lib.repositories.user_repository import create, get_by_name


async def create_user(user):
    if not user or not user['name']:
        raise InvalidBodyError()
    name = user['name'].replace(' ', '')
    name = name.lower()

    existing_user = await get_by_name(name)
    if not existing_user is None:
        raise UserAlreadyExistsError(name)

    new_user = await create(name)
    return new_user