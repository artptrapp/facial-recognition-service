class InvalidImageError(Exception):
    name = 'InvalidImageError'
    related_status_code = 422
    message = ''

    def __init__(self, file_name) -> None:
        message = f'The image {file_name} is not valid.'
        super().__init__(message)
        self.message = message

    def to_json(self):
        return {
            'name': self.name,
            'status_code': self.related_status_code,
            'message': self.message
        }