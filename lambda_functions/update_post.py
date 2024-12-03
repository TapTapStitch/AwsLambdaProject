import json
from lambda_functions.lambda_layer.utils import PostService


def lambda_handler(event, context):
    post_id = event["pathParameters"]["id"]
    update_data = json.loads(event["body"])

    post_service = PostService()
    updated_post = post_service.update_post(post_id, update_data)
    if updated_post:
        return {"statusCode": 200, "body": json.dumps(updated_post)}
    else:
        return {"statusCode": 404, "body": json.dumps({"error": "Post not found"})}
