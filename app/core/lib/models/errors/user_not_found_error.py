class UserNotFoundError(Exception):
    name = 'UserNotFoundError'
    related_status_code = 404
    message = ''

    def __init__(self, user_id) -> None:
        message = f'User with the id {user_id} was not found in the database.'
        super().__init__(message)
        self.message = message

    def to_json(self):
        return {
            'name': self.name,
            'status_code': self.related_status_code,
            'message': self.message
        }