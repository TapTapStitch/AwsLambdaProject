import pytest
from jsonschema import ValidationError
from lambda_functions.lambda_layer.decorators import exception_handler

class MockService:
    def _response(self, success, error=None):
        return {"success": success, "error": error}

@exception_handler
def mock_function_no_exception(self):
    return self._response(success=True)

@exception_handler
def mock_function_validation_error(self):
    raise ValidationError("Invalid data")

@exception_handler
def mock_function_generic_exception(self):
    raise Exception("Something went wrong")

def test_exception_handler_no_exception():
    service = MockService()
    result = mock_function_no_exception(service)
    assert result["success"] is True
    assert result["error"] is None

def test_exception_handler_validation_error():
    service = MockService()
    result = mock_function_validation_error(service)
    assert result["success"] is False
    assert "Validation error: Invalid data" in result["error"]

def test_exception_handler_generic_exception():
    service = MockService()
    result = mock_function_generic_exception(service)
    assert result["success"] is False
    assert "Something went wrong" in result["error"]