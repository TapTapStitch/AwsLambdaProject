import json
from lambda_functions.lambda_layer.utils import PostService


def lambda_handler(event, context):
    post_data = json.loads(event["body"])
    title = post_data.get("title")
    body = post_data.get("body")
    tags = post_data.get("tags", [])

    post_service = PostService()
    response = post_service.create_post(title, body, tags)

    if response["success"]:
        return {"statusCode": 201, "body": json.dumps(response["data"])}
    else:
        error_message = response["error"]
        if "Validation error" in error_message:
            return {"statusCode": 422, "body": json.dumps({"error": error_message})}
        else:
            return {
                "statusCode": 500,
                "body": json.dumps(
                    {"error": "Error creating post", "details": error_message}
                ),
            }
