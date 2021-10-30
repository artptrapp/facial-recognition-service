from app.core.lib.utils.image_utils import validate_file_as_image
from ..repositories import user_repository
from ..models.errors.invalid_image_error import InvalidImageError
from ..models.errors.user_not_found_error import UserNotFoundError
from fastapi import File, UploadFile
from ..utils.image_utils import validate_file_as_image
from ..image_processing.compare_images import check_image_match


async def compare_user_image(username: str, image: UploadFile = File(...)):
    if not validate_file_as_image(image):
        raise InvalidImageError(image.filename)
    user = await user_repository.get_by_name(username)
    if user is None:
        raise UserNotFoundError(username)

    return await check_image_match(user, image)
