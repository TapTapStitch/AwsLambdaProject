import json
from lambda_functions.lambda_layer.utils import PostService


def lambda_handler(event, context):
    post_service = PostService()
    posts = post_service.get_all_posts()
    return {"statusCode": 200, "body": json.dumps(posts)}
