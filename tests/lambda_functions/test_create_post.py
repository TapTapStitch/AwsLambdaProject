import pytest
import json
from lambda_functions.create_post import create_post


class MockPostService:
    def __init__(self, mock_response):
        self.mock_response = mock_response

    def create_post(self, title, body, tags):
        return self.mock_response


@pytest.fixture
def mock_post_service_success(monkeypatch):
    mock_response = {
        "success": True,
        "data": {
            "id": "1",
            "title": "Post 1",
            "body": "Body 1",
            "tags": ["tag1", "tag2"],
            "createdDate": "2023-01-01T12:00:00Z",
        },
    }
    monkeypatch.setattr(
        "lambda_functions.create_post.PostService",
        lambda: MockPostService(mock_response),
    )


@pytest.fixture
def mock_post_service_validation_error(monkeypatch):
    mock_response = {
        "success": False,
        "error": "Validation error: Title is required",
    }
    monkeypatch.setattr(
        "lambda_functions.create_post.PostService",
        lambda: MockPostService(mock_response),
    )


@pytest.fixture
def mock_post_service_error(monkeypatch):
    mock_response = {
        "success": False,
        "error": "Database connection failed",
    }
    monkeypatch.setattr(
        "lambda_functions.create_post.PostService",
        lambda: MockPostService(mock_response),
    )


def test_create_post_success(mock_post_service_success):
    event = {
        "body": json.dumps(
            {
                "title": "Post 1",
                "body": "This is the body of Post 1",
                "tags": ["tag1", "tag2"],
            }
        )
    }

    result = create_post(event)

    assert result["statusCode"] == 201
    body = json.loads(result["body"])
    assert body["id"] == "1"
    assert body["title"] == "Post 1"
    assert body["tags"] == ["tag1", "tag2"]


def test_create_post_validation_error(mock_post_service_validation_error):
    event = {
        "body": json.dumps(
            {"title": "", "body": "This is a post with no title", "tags": ["tag1"]}
        )
    }

    result = create_post(event)

    assert result["statusCode"] == 422
    body = json.loads(result["body"])
    assert body["error"] == "Validation error: Title is required"


def test_create_post_error(mock_post_service_error):
    event = {
        "body": json.dumps(
            {"title": "Post 1", "body": "This is the body of Post 1", "tags": ["tag1"]}
        )
    }

    result = create_post(event)

    assert result["statusCode"] == 500
    body = json.loads(result["body"])
    assert body["error"] == "Error creating post"
    assert body["details"] == "Database connection failed"
