import json
from lambda_functions.lambda_layer.utils import PostService


def delete_post(event):
    post_id = event["pathParameters"]["id"]
    post_service = PostService()
    try:
        success = post_service.delete_post(post_id)
        if success:
            return {"statusCode": 204, "body": ""}
    except Exception as e:
        if "not found" in str(e).lower():
            return {"statusCode": 404, "body": json.dumps({"error": "Post not found"})}
        else:
            return {
                "statusCode": 500,
                "body": json.dumps({"error": "Error deleting post", "details": str(e)}),
            }
