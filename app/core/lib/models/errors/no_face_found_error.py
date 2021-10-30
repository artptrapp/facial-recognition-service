class NoFaceFoundError(Exception):
    name = 'NoFaceFoundError'
    related_status_code = 400
    message = ''

    def __init__(self) -> None:
        message = f'No face was detected on the provided picture. Check if the picture has a clear face on it, and has decent quality.'
        super().__init__(message)
        self.message = message

    def to_json(self):
        return {
            'name': self.name,
            'status_code': self.related_status_code,
            'message': self.message
        }