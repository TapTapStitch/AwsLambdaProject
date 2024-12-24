import pytest
from pydantic import ValidationError
from lambda_layer.validators import PostModel


def test_post_model_valid_data():
    valid_data = {
        "title": "Valid Title",
        "body": "This is a valid body.",
        "tags": ["tag1", "tag2"],
    }

    post = PostModel(**valid_data)
    assert post.title == "Valid Title"
    assert post.body == "This is a valid body."
    assert post.tags == ["tag1", "tag2"]


def test_post_model_missing_optional_field():
    valid_data = {"title": "Valid Title", "body": "This is a valid body."}

    post = PostModel(**valid_data)
    assert post.title == "Valid Title"
    assert post.body == "This is a valid body."
    assert post.tags == []


def test_post_model_invalid_title_length():
    invalid_data = {
        "title": "",
        "body": "This is a valid body.",
    }

    with pytest.raises(ValidationError) as exc_info:
        PostModel(**invalid_data)

    assert "title" in str(exc_info.value)


def test_post_model_invalid_body_length():
    invalid_data = {
        "title": "Valid Title",
        "body": "x" * 2001,
    }

    with pytest.raises(ValidationError) as exc_info:
        PostModel(**invalid_data)

    assert "body" in str(exc_info.value)


def test_post_model_invalid_tags_type():
    invalid_data = {
        "title": "Valid Title",
        "body": "This is a valid body.",
        "tags": "not-a-list",
    }

    with pytest.raises(ValidationError) as exc_info:
        PostModel(**invalid_data)

    assert "tags" in str(exc_info.value)
