import json
from lambda_functions.lambda_layer.utils import PostService


def get_posts():
    post_service = PostService()
    response = post_service.get_all_posts()

    if response["success"]:
        sorted_posts = sorted(response["data"], key=lambda x: x["createdDate"])
        return {"statusCode": 200, "body": json.dumps(sorted_posts)}
    else:
        error_message = response["error"]
        return {
            "statusCode": 500,
            "body": json.dumps(
                {"error": "Error retrieving posts", "details": error_message}
            ),
        }
