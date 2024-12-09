from jsonschema import ValidationError


def exception_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValidationError as ve:
            return args[0]._response(
                success=False, error=f"Validation error: {ve.message}"
            )
        except Exception as e:
            return args[0]._response(success=False, error=str(e))

    return wrapper
