from flask import request


class BasicException(Exception):
    status_code = 0
    message = 'Error'

    def __init__(self, message=None, status_code=None):
        super().__init__(message)
        self.message = message
        request.status = self.status_code
        if status_code is not None:
            self.status_code = status_code


class NotFound(BasicException):
    status_code = 404
    message = 'Not Found'


class AuthError(BasicException):
    status_code = 401
    message = 'Authorization error'


class Forbidden(BasicException):
    status_code = 403
    message = 'Forbidden'


class IntegrityError(BasicException):
    status_code = 400
    message = 'Integrity error'


class ValidateError(BasicException):
    status_code = 400
    message = 'Validation error'
