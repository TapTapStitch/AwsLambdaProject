import pytest
import json
from lambda_functions.get_post import lambda_handler


class MockPostService:
    def __init__(self, mock_response):
        self.mock_response = mock_response

    def get_post_by_id(self, post_id):
        return self.mock_response


@pytest.fixture
def mock_post_service_success(monkeypatch):
    mock_response = {
        "success": True,
        "data": {
            "id": "1",
            "title": "Post 1",
            "body": "Body 1",
            "createdDate": "2023-01-01T12:00:00Z",
        },
    }
    monkeypatch.setattr(
        "lambda_functions.get_post.PostService", lambda: MockPostService(mock_response)
    )


@pytest.fixture
def mock_post_service_not_found(monkeypatch):
    mock_response = {
        "success": False,
        "error": "Post not found",
    }
    monkeypatch.setattr(
        "lambda_functions.get_post.PostService", lambda: MockPostService(mock_response)
    )


@pytest.fixture
def mock_post_service_error(monkeypatch):
    mock_response = {
        "success": False,
        "error": "Database connection failed",
    }
    monkeypatch.setattr(
        "lambda_functions.get_post.PostService", lambda: MockPostService(mock_response)
    )


def test_get_post_success(mock_post_service_success):
    event = {"pathParameters": {"postId": "1"}}
    result = lambda_handler(event, None)

    assert result["statusCode"] == 200
    body = json.loads(result["body"])
    assert body["id"] == "1"
    assert body["title"] == "Post 1"


def test_get_post_not_found(mock_post_service_not_found):
    event = {"pathParameters": {"postId": "999"}}
    result = lambda_handler(event, None)

    assert result["statusCode"] == 404
    body = json.loads(result["body"])
    assert body["error"] == "Post not found"


def test_get_post_error(mock_post_service_error):
    event = {"pathParameters": {"postId": "1"}}
    result = lambda_handler(event, None)

    assert result["statusCode"] == 500
    body = json.loads(result["body"])
    assert body["error"] == "Error retrieving post"
    assert body["details"] == "Database connection failed"
