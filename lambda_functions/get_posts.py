import json
from lambda_functions.lambda_layer.utils import PostService


def get_posts():
    post_service = PostService()
    try:
        posts = post_service.get_all_posts()
        return {"statusCode": 200, "body": json.dumps(posts)}
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Error retrieving posts", "details": str(e)}),
        }
