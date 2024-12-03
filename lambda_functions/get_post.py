import json
from lambda_functions.lambda_layer.utils import PostService


def lambda_handler(event, context):
    post_id = event["pathParameters"]["id"]
    post_service = PostService()
    post = post_service.get_post_by_id(post_id)
    if post:
        return {"statusCode": 200, "body": json.dumps(post)}
    else:
        return {"statusCode": 404, "body": json.dumps({"error": "Post not found"})}
