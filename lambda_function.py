import json
from lambda_functions.get_posts import get_posts
from lambda_functions.get_post import get_post
from lambda_functions.create_post import create_post
from lambda_functions.update_post import update_post
from lambda_functions.delete_post import delete_post


def lambda_handler(event, context):
    http_method = event.get("httpMethod")
    path = event.get("path")

    if http_method == "GET" and path == "/posts":
        return get_posts()
    elif http_method == "GET" and path.startswith("/post/"):
        post_id = path.split("/")[-1]
        return get_post(post_id)
    elif http_method == "POST" and path == "/posts":
        return create_post(event)
    elif http_method == "PATCH" and path.startswith("/post/"):
        post_id = path.split("/")[-1]
        return update_post(post_id, event)
    elif http_method == "DELETE" and path.startswith("/post/"):
        post_id = path.split("/")[-1]
        return delete_post(post_id)
    else:
        return {"statusCode": 400, "body": json.dumps({"error": "Invalid route"})}
