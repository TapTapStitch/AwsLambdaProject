import boto3
import uuid
from datetime import datetime, timezone
from boto3.dynamodb.conditions import Key
from pydantic import BaseModel, Field, ValidationError
from typing import List, Optional


class PostModel(BaseModel):
    title: str = Field(..., max_length=200)
    body: str = Field(..., max_length=2000)
    tags: Optional[List[str]] = None


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
        try:
            post_data = PostModel(title=title, body=body, tags=tags).model_dump()

            post_id = str(uuid.uuid4())
            current_time = datetime.now(timezone.utc).isoformat()

            post_data.update(
                {
                    "id": post_id,
                    "createdDate": current_time,
                    "updatedDate": current_time,
                }
            )

            self.table.put_item(Item=post_data)
            return {"statusCode": 201, "body": post_data}
        except ValidationError as e:
            return {
                "statusCode": 422,
                "body": {"error": "Validation error", "details": e.errors()},
            }
        except Exception as e:
            print(f"Error creating post: {e}")
            return {"statusCode": 500, "body": {"error": "Internal server error"}}

    def update_post(self, post_id, update_data):
        try:
            validated_data = PostModel(**update_data).model_dump(exclude_unset=True)
            validated_data["updatedDate"] = datetime.now(timezone.utc).isoformat()

            expression = "SET " + ", ".join(f"{k}=:{k}" for k in validated_data.keys())
            expression_values = {f":{k}": v for k, v in validated_data.items()}

            self.table.update_item(
                Key={"id": post_id},
                UpdateExpression=expression,
                ExpressionAttributeValues=expression_values,
            )
            return self.get_post_by_id(post_id)
        except ValidationError as e:
            return {
                "statusCode": 422,
                "body": {"error": "Validation error", "details": e.errors()},
            }
        except Exception as e:
            print(f"Error updating post {post_id}: {e}")
            return {"statusCode": 500, "body": {"error": "Internal server error"}}

    def delete_post(self, post_id):
        try:
            self.table.delete_item(Key={"id": post_id})
            return True
        except Exception as e:
            print(f"Error deleting post {post_id}: {e}")
            return False
