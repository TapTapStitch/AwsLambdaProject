import pytest
from moto import mock_dynamodb
import boto3
from lambda_functions.lambda_layer.utils import PostService
from datetime import datetime, timezone


@pytest.fixture
def dynamodb():
    with mock_dynamodb():
        yield boto3.resource("dynamodb", region_name="eu-north-1")


@pytest.fixture
def posts_table(dynamodb):
    table_name = "PostsTable"
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
        ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
    )
    table.meta.client.get_waiter("table_exists").wait(TableName=table_name)
    return table


@pytest.fixture
def post_service(posts_table):
    return PostService(table_name=posts_table.name)


def test_create_post_success(post_service):
    before_creation = datetime.now(timezone.utc)

    response = post_service.create_post(
        title="Test Title", body="Test Body", tags=["test", "post"]
    )

    after_creation = datetime.now(timezone.utc)

    assert response["success"]
    assert response["data"]["title"] == "Test Title"
    assert response["data"]["body"] == "Test Body"
    assert response["data"]["tags"] == ["test", "post"]

    created_date = datetime.fromisoformat(response["data"]["createdDate"])

    assert before_creation <= created_date <= after_creation


def test_create_post_validation_error(post_service):
    response = post_service.create_post(title="", body="")
    assert not response["success"]
    assert "Validation error" in response["error"]


def test_get_all_posts_empty(post_service):
    response = post_service.get_all_posts()
    assert response["success"]
    assert response["data"] == []


def test_get_all_posts(post_service):
    post_service.create_post(title="Test Title", body="Test Body")
    response = post_service.get_all_posts()
    assert response["success"]
    assert len(response["data"]) == 1


def test_get_post_by_id_success(post_service):
    create_response = post_service.create_post(title="Test Title", body="Test Body")
    post_id = create_response["data"]["id"]
    response = post_service.get_post_by_id(post_id)
    assert response["success"]
    assert response["data"]["id"] == post_id


def test_get_post_by_id_not_found(post_service):
    response = post_service.get_post_by_id("non-existent-id")
    assert not response["success"]
    assert response["error"] == "Post not found"


def test_update_post_success(post_service):
    create_response = post_service.create_post(title="Test Title", body="Test Body")
    post_id = create_response["data"]["id"]

    before_update = datetime.now(timezone.utc)

    update_response = post_service.update_post(
        post_id, {"title": "Updated Title", "body": "Updated Body"}
    )

    after_update = datetime.now(timezone.utc)

    assert update_response["success"]
    assert update_response["data"]["title"] == "Updated Title"

    updated_date = datetime.fromisoformat(update_response["data"]["updatedDate"])

    assert before_update <= updated_date <= after_update


def test_update_post_validation_error(post_service):
    create_response = post_service.create_post(title="Test Title", body="Test Body")
    post_id = create_response["data"]["id"]
    update_response = post_service.update_post(post_id, {"title": "", "body": ""})
    assert not update_response["success"]
    assert "Validation error" in update_response["error"]


def test_delete_post_success(post_service):
    create_response = post_service.create_post(title="Test Title", body="Test Body")
    post_id = create_response["data"]["id"]
    delete_response = post_service.delete_post(post_id)
    assert delete_response["success"]
    assert delete_response["data"] == "Post deleted successfully"


def test_delete_post_not_found(post_service):
    delete_response = post_service.delete_post("non-existent-id")
    assert delete_response["success"]
