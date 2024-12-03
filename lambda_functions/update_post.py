import json
from lambda_functions.lambda_layer.utils import PostService


def update_post(event):
    post_id = event["pathParameters"]["id"]
    update_data = json.loads(event["body"])

    post_service = PostService()
    try:
        updated_post = post_service.update_post(post_id, update_data)
        if updated_post:
            return {"statusCode": 200, "body": json.dumps(updated_post)}
        else:
            return {"statusCode": 404, "body": json.dumps({"error": "Post not found"})}
    except ValueError as ve:
        return {
            "statusCode": 422,
            "body": json.dumps({"error": "Validation error", "details": str(ve)}),
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Error updating post", "details": str(e)}),
        }
