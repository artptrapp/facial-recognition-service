from app.core.lib.models.errors.no_face_found_error import NoFaceFoundError
import face_recognition
import uuid
import pickle

from fastapi import UploadFile
from ..utils.path_utils import get_project_root

DATA_PATH = str(get_project_root()).replace('/core/lib', '/data/test-pictures')
TEMP_FOLDER = str(get_project_root()).replace('/core/lib', '/temp')
MATCH_THRESHOLD = 0.5

async def get_image_encoding(image: UploadFile):
    temp_image_name = await save_post_image_to_disk(image)
    comparison_image = face_recognition.load_image_file(temp_image_name)
    encodings = face_recognition.face_encodings(comparison_image)
    return encodings

async def check_image_match(user, candidate_image: UploadFile):
    # First, save the candidate image to disk
    temp_image_name = await save_post_image_to_disk(candidate_image)
    comparison_image = face_recognition.load_image_file(temp_image_name)
    # Checks if there is at least one identifiable face on the provided photo
    comparison_encodings = face_recognition.face_encodings(comparison_image)
    if len(comparison_encodings) == 0:
        raise NoFaceFoundError()

    comparison_encoding_to_use = comparison_encodings[0]

    i = 0
    percentage_match_sum = 0
    match_count = 0
    euclidean_sum = 0

    existing_faces = user.get('known_faces')
    if existing_faces is None:
        raise NoFaceFoundError()

    for binary_image in user['known_faces']:
        parsed = pickle.loads(binary_image)
        # And finally, compare them
        try:
            is_match = face_recognition.compare_faces(parsed, comparison_encoding_to_use, tolerance=MATCH_THRESHOLD)[0]
            face_distance = face_recognition.face_distance(parsed, comparison_encoding_to_use)[0]
            face_match_percentage = (1 - face_distance) * 100

            match_count += 1 if is_match else 0
            euclidean_sum += face_distance
            percentage_match_sum += face_match_percentage
            i += 1
        except:
            pass

    euclidean_sum = euclidean_sum / i
    percentage_match_sum = percentage_match_sum / i

    return {
        'match_count': match_count,
        'total_comparisons': i,
        'average_euclidean_distance': euclidean_sum,
        'average_match_percentage': percentage_match_sum,
        'is_likely_match': bool(percentage_match_sum >= MATCH_THRESHOLD * 100)
    }


def load_user_file(path: str):
    return face_recognition.load_image_file(f'{DATA_PATH}/{path}')

async def save_post_image_to_disk(image: UploadFile):
    raw_file = await image.read()
    filename = f'{TEMP_FOLDER}/{uuid.uuid4()}.png'
    with open(filename, 'w+b') as f:
        f.write(raw_file)
    return filename