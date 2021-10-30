from fastapi import File, UploadFile

allowed_content_types = [
    'image/jpeg',
    'image/jpg',
    'image/png'
]

def validate_file_as_image(image: UploadFile = File(...)):
    if not image.content_type in allowed_content_types:
        return False
    return True
