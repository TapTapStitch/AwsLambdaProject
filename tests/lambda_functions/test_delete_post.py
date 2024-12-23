import pytest
import json
from lambda_functions.delete_post.delete_post import lambda_handler


class MockPostService:
    def __init__(self, mock_response):
        self.mock_response = mock_response

    def delete_post(self, post_id):
        return self.mock_response


@pytest.fixture
def mock_post_service_success(monkeypatch):
    mock_response = {"success": True, "data": None}
    monkeypatch.setattr(
        "lambda_functions.delete_post.PostService",
        lambda: MockPostService(mock_response),
    )


@pytest.fixture
def mock_post_service_not_found(monkeypatch):
    mock_response = {
        "success": False,
        "error": "Post not found",
    }
    monkeypatch.setattr(
        "lambda_functions.delete_post.PostService",
        lambda: MockPostService(mock_response),
    )


@pytest.fixture
def mock_post_service_error(monkeypatch):
    mock_response = {
        "success": False,
        "error": "Database connection failed",
    }
    monkeypatch.setattr(
        "lambda_functions.delete_post.PostService",
        lambda: MockPostService(mock_response),
    )


def test_delete_post_success(mock_post_service_success):
    event = {"pathParameters": {"id": "1"}}

    result = lambda_handler(event, None)

    assert result["statusCode"] == 204
    assert result["body"] == ""


def test_delete_post_not_found(mock_post_service_not_found):
    event = {"pathParameters": {"id": "999"}}

    result = lambda_handler(event, None)

    assert result["statusCode"] == 404
    body = json.loads(result["body"])
    assert body["error"] == "Post not found"


def test_delete_post_error(mock_post_service_error):
    event = {"pathParameters": {"id": "1"}}

    result = lambda_handler(event, None)

    assert result["statusCode"] == 500
    body = json.loads(result["body"])
    assert body["error"] == "Error deleting post"
    assert body["details"] == "Database connection failed"
