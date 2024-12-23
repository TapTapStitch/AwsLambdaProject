import json
from utils import PostService


def lambda_handler(event, context):
    query_params = event.get("queryStringParameters") or {}
    tags = query_params.get("tags")
    limit = query_params.get("limit")
    post_service = PostService()
    response = post_service.get_all_posts()
    if response["success"]:
        posts = response["data"]
        if tags:
            tag_list = [tag.strip() for tag in tags.split(",")]
            posts = [
                post
                for post in posts
                if any(tag in post.get("tags", []) for tag in tag_list)
            ]
        sorted_posts = sorted(posts, key=lambda x: x["createdDate"])
        if limit:
            try:
                limit = int(limit)
                sorted_posts = sorted_posts[:limit]
            except ValueError:
                return {
                    "statusCode": 400,
                    "body": json.dumps({"error": "Invalid limit parameter"}),
                }
        public_posts = [
            {key: value for key, value in post.items() if key != "id"}
            for post in sorted_posts
        ]
        return {"statusCode": 200, "body": json.dumps(public_posts)}
    else:
        error_message = response["error"]
        return {
            "statusCode": 500,
            "body": json.dumps(
                {"error": "Error retrieving posts", "details": error_message}
            ),
        }
