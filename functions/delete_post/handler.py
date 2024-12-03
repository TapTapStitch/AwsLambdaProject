import json
from layer.shared.dynamo import PostService


def lambda_handler(event, context):
    post_id = event["pathParameters"]["id"]

    post_service = PostService()
    success = post_service.delete_post(post_id)
    if success:
        return {"statusCode": 204, "body": ""}
    else:
        return {"statusCode": 404, "body": json.dumps({"error": "Post not found"})}
