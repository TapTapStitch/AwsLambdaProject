import json
from lambda_functions.lambda_layer.utils import PostService


def delete_post(post_id):
    post_service = PostService()
    success = post_service.delete_post(post_id)
    if success:
        return {"statusCode": 204, "body": ""}
    else:
        return {"statusCode": 404, "body": json.dumps({"error": "Post not found"})}
