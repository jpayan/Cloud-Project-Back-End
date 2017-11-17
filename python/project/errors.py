class UnauthorizedError(Exception):
    def __init__(self):
        self.code = 403
        self.message = 'User is not authorized to do this action.'
