import boto3
import uuid
from datetime import datetime, timezone
from boto3.dynamodb.conditions import Key


class PostService:
    def __init__(self, table_name="PostsTable", region_name="eu-north-1"):
        self.dynamodb = boto3.resource("dynamodb", region_name=region_name)
        self.table = self.dynamodb.Table(table_name)

    def get_all_posts(self):
        try:
            response = self.table.scan()
            return response.get("Items", [])
        except Exception as e:
            print(f"Error getting all posts: {e}")
            return []

    def get_post_by_id(self, post_id):
        try:
            response = self.table.get_item(Key={"id": post_id})
            return response.get("Item", None)
        except Exception as e:
            print(f"Error getting post by ID {post_id}: {e}")
            return None

    def create_post(self, title, body, tags=None):
        if tags is None:
            tags = []
        post_id = str(uuid.uuid4())
        current_time = datetime.now(timezone.utc).isoformat()
        post_data = {
            "id": post_id,
            "title": title,
            "body": body,
            "tags": tags,
            "createdDate": current_time,
            "updatedDate": current_time
        }
        try:
            self.table.put_item(Item=post_data)
            return post_data
        except Exception as e:
            print(f"Error creating post: {e}")
            return None

    def update_post(self, post_id, update_data):
        try:
            update_data["updatedDate"] = datetime.now(timezone.utc).isoformat()
            expression = "SET " + ", ".join(f"{k}=:{k}" for k in update_data.keys())
            expression_values = {f":{k}": v for k, v in update_data.items()}

            self.table.update_item(
                Key={"id": post_id},
                UpdateExpression=expression,
                ExpressionAttributeValues=expression_values,
            )
            return self.get_post_by_id(post_id)
        except Exception as e:
            print(f"Error updating post {post_id}: {e}")
            return None