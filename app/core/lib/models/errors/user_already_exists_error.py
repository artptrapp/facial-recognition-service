class UserAlreadyExistsError(Exception):
    name = 'UserAlreadyExistsError'
    related_status_code = 400
    message = ''

    def __init__(self, user_name) -> None:
        message = f'User with the name {user_name} already exists in the database.'
        super().__init__(message)
        self.message = message

    def to_json(self):
        return {
            'name': self.name,
            'status_code': self.related_status_code,
            'message': self.message
        }