import pytest
import json
from lambda_functions.update_post.update_post import lambda_handler


class MockPostService:
    def __init__(self, mock_response):
        self.mock_response = mock_response

    def update_post(self, post_id, update_data):
        return self.mock_response


@pytest.fixture
def mock_post_service_success(monkeypatch):
    mock_response = {
        "success": True,
        "data": {
            "id": "1",
            "title": "Updated Post Title",
            "body": "Updated post body",
            "tags": ["tag1", "tag2"],
            "createdDate": "2023-01-01T12:00:00Z",
        },
    }
    monkeypatch.setattr(
        "lambda_functions.update_post.PostService",
        lambda: MockPostService(mock_response),
    )


@pytest.fixture
def mock_post_service_validation_error(monkeypatch):
    mock_response = {
        "success": False,
        "error": "Validation error: Title is required",
    }
    monkeypatch.setattr(
        "lambda_functions.update_post.PostService",
        lambda: MockPostService(mock_response),
    )


@pytest.fixture
def mock_post_service_not_found(monkeypatch):
    mock_response = {
        "success": False,
        "error": "Post not found",
    }
    monkeypatch.setattr(
        "lambda_functions.update_post.PostService",
        lambda: MockPostService(mock_response),
    )


@pytest.fixture
def mock_post_service_error(monkeypatch):
    mock_response = {
        "success": False,
        "error": "Database connection failed",
    }
    monkeypatch.setattr(
        "lambda_functions.update_post.PostService",
        lambda: MockPostService(mock_response),
    )


def test_update_post_success(mock_post_service_success):
    event = {
        "pathParameters": {"id": "1"},
        "body": json.dumps(
            {
                "title": "Updated Post Title",
                "body": "Updated post body",
                "tags": ["tag1", "tag2"],
            }
        ),
    }

    result = lambda_handler(event, None)

    assert result["statusCode"] == 200
    body = json.loads(result["body"])
    assert body["id"] == "1"
    assert body["title"] == "Updated Post Title"
    assert body["tags"] == ["tag1", "tag2"]


def test_update_post_validation_error(mock_post_service_validation_error):
    event = {
        "pathParameters": {"id": "1"},
        "body": json.dumps(
            {"title": "", "body": "Updated post body", "tags": ["tag1"]}
        ),
    }

    result = lambda_handler(event, None)

    assert result["statusCode"] == 422
    body = json.loads(result["body"])
    assert body["error"] == "Validation error"
    assert body["details"] == "Validation error: Title is required"


def test_update_post_not_found(mock_post_service_not_found):
    event = {
        "pathParameters": {"id": "999"},
        "body": json.dumps(
            {"title": "New Title", "body": "New body text", "tags": ["tag1"]}
        ),
    }

    result = lambda_handler(event, None)

    assert result["statusCode"] == 404
    body = json.loads(result["body"])
    assert body["error"] == "Post not found"


def test_update_post_error(mock_post_service_error):
    event = {
        "pathParameters": {"id": "1"},
        "body": json.dumps(
            {
                "title": "Post Title",
                "body": "This is the body of the post",
                "tags": ["tag1"],
            }
        ),
    }

    result = lambda_handler(event, None)

    assert result["statusCode"] == 500
    body = json.loads(result["body"])
    assert body["error"] == "Error updating post"
    assert body["details"] == "Database connection failed"
