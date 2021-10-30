class InvalidBodyError(Exception):
    name = 'InvalidBodyError'
    related_status_code = 400
    message = ''

    def __init__(self) -> None:
        message = f'The request body is invalid'
        super().__init__(message)
        self.message = message

    def to_json(self):
        return {
            'name': self.name,
            'status_code': self.related_status_code,
            'message': self.message
        }