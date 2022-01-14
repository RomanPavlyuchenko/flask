import jsonschema
from flask import request

import errors


def validate(source, schema):

    def decorator(func):

        def wrapper(*args, **kwargs):
            try:
                test = request
                jsonschema.validate(
                    instance=getattr(request, source), schema=schema,
                )
            except jsonschema.ValidationError as msg:
                raise errors.ValidateError

            return func(*args, **kwargs)
        return wrapper
    return decorator
