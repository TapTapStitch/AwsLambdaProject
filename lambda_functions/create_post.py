import json
from lambda_functions.lambda_layer.utils import PostService


def create_post(event):
    post_data = json.loads(event["body"])
    title = post_data.get("title")
    body = post_data.get("body")
    tags = post_data.get("tags", [])

    post_service = PostService()
    try:
        new_post = post_service.create_post(title, body, tags)
        return {"statusCode": 201, "body": json.dumps(new_post)}
    except ValueError as ve:
        return {"statusCode": 422, "body": json.dumps({"error": str(ve)})}
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Error creating post", "details": str(e)}),
        }
