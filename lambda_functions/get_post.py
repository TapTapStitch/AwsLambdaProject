import json
from lambda_layer.utils import PostService


def lambda_handler(event, context):
    post_id = event["pathParameters"]["id"]
    post_service = PostService()
    response = post_service.get_post_by_id(post_id)

    if response["success"]:
        return {"statusCode": 200, "body": json.dumps(response["data"])}
    else:
        error_message = response["error"]
        if "not found" in error_message.lower():
            return {"statusCode": 404, "body": json.dumps({"error": "Post not found"})}
        else:
            return {
                "statusCode": 500,
                "body": json.dumps(
                    {"error": "Error retrieving post", "details": error_message}
                ),
            }
