import json
from lambda_functions.lambda_layer.utils import PostService


def lambda_handler(event, context):
    post_id = event["pathParameters"]["id"]
    post_service = PostService()
    response = post_service.delete_post(post_id)

    if response["success"]:
        return {"statusCode": 204, "body": ""}
    else:
        error_message = response["error"]
        if "not found" in error_message.lower():
            return {"statusCode": 404, "body": json.dumps({"error": "Post not found"})}
        else:
            return {
                "statusCode": 500,
                "body": json.dumps(
                    {"error": "Error deleting post", "details": error_message}
                ),
            }