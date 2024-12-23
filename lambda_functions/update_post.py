import json
from lambda_layer.utils import PostService


def lambda_handler(event, context):
    post_id = event["pathParameters"]["id"]
    update_data = json.loads(event["body"])

    post_service = PostService()
    response = post_service.update_post(post_id, update_data)

    if response["success"]:
        return {"statusCode": 200, "body": json.dumps(response["data"])}
    else:
        error_message = response["error"]
        if "error" in error_message:
            return {
                "statusCode": 422,
                "body": json.dumps(
                    {"error": "Validation error", "details": error_message}
                ),
            }
        elif "not found" in error_message.lower():
            return {"statusCode": 404, "body": json.dumps({"error": "Post not found"})}
        else:
            return {
                "statusCode": 500,
                "body": json.dumps(
                    {"error": "Error updating post", "details": error_message}
                ),
            }
