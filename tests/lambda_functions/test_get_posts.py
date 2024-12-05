import pytest
import json
from lambda_functions.get_posts import get_posts


class MockPostService:
    def __init__(self, mock_response):
        self.mock_response = mock_response

    def get_all_posts(self):
        return self.mock_response


@pytest.fixture
def mock_post_service_success(monkeypatch):
    mock_response = {
        "success": True,
        "data": [
            {
                "id": "1",
                "title": "Post 1",
                "body": "Body 1",
                "createdDate": "2023-01-01T12:00:00Z",
                "tags": ["tech", "news"],
            },
            {
                "id": "2",
                "title": "Post 2",
                "body": "Body 2",
                "createdDate": "2023-01-02T12:00:00Z",
                "tags": ["health", "news"],
            },
        ],
    }
    monkeypatch.setattr(
        "lambda_functions.get_posts.PostService", lambda: MockPostService(mock_response)
    )


@pytest.fixture
def mock_post_service_error(monkeypatch):
    mock_response = {
        "success": False,
        "error": "Database connection failed",
    }
    monkeypatch.setattr(
        "lambda_functions.get_posts.PostService", lambda: MockPostService(mock_response)
    )


def test_get_posts_success(mock_post_service_success):
    event = {"queryStringParameters": None}
    result = get_posts(event)

    assert result["statusCode"] == 200
    body = json.loads(result["body"])
    assert len(body) == 2
    assert body[0]["id"] == "1"
    assert body[1]["id"] == "2"


def test_get_posts_with_tags(mock_post_service_success):
    event = {"queryStringParameters": {"tags": "tech"}}
    result = get_posts(event)

    assert result["statusCode"] == 200
    body = json.loads(result["body"])
    assert len(body) == 1
    assert body[0]["id"] == "1"


def test_get_posts_with_limit(mock_post_service_success):
    event = {"queryStringParameters": {"limit": "1"}}
    result = get_posts(event)

    assert result["statusCode"] == 200
    body = json.loads(result["body"])
    assert len(body) == 1
    assert body[0]["id"] == "1"


def test_get_posts_with_invalid_limit(mock_post_service_success):
    event = {"queryStringParameters": {"limit": "invalid"}}
    result = get_posts(event)

    assert result["statusCode"] == 400
    body = json.loads(result["body"])
    assert "error" in body
    assert body["error"] == "Invalid limit parameter"


def test_get_posts_error(mock_post_service_error):
    event = {"queryStringParameters": None}
    result = get_posts(event)

    assert result["statusCode"] == 500
    body = json.loads(result["body"])
    assert "error" in body
    assert body["error"] == "Error retrieving posts"
    assert body["details"] == "Database connection failed"
