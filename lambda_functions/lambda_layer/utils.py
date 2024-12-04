import boto3
import uuid
from datetime import datetime, timezone
from boto3.dynamodb.conditions import Key
from jsonschema import validate, ValidationError


class PostService:
    def __init__(self, table_name="PostsTable", region_name="eu-north-1"):
        self.dynamodb = boto3.resource("dynamodb", region_name=region_name)
        self.table = self.dynamodb.Table(table_name)

    def _validate_post_data(self, data):
        post_schema = {
            "type": "object",
            "properties": {
                "title": {"type": "string", "maxLength": 200},
                "body": {"type": "string", "maxLength": 2000},
                "tags": {"type": "array", "items": {"type": "string"}},
            },
            "required": ["title", "body"],
            "additionalProperties": False,
        }
        validate(instance=data, schema=post_schema)

    def _format_post_data(self, post_data):
        return {
            "id": post_data.get("id"),
            "title": post_data.get("title"),
            "body": post_data.get("body"),
            "createdDate": post_data.get("createdDate"),
            "updatedDate": post_data.get("updatedDate"),
            "tags": post_data.get("tags", []),
        }

    def _response(self, success, data=None, error=None):
        return {"success": success, "data": data, "error": error}

    def get_all_posts(self):
        try:
            response = self.table.scan()
            items = response.get("Items", [])
            formatted_items = [self._format_post_data(item) for item in items]
            return self._response(success=True, data=formatted_items)
        except Exception as e:
            return self._response(success=False, error=str(e))

    def get_post_by_id(self, post_id):
        try:
            response = self.table.get_item(Key={"id": post_id})
            item = response.get("Item", None)
            if item:
                formatted_item = self._format_post_data(item)
                return self._response(success=True, data=formatted_item)
            else:
                return self._response(success=False, error="Post not found")
        except Exception as e:
            return self._response(success=False, error=str(e))

    def create_post(self, title, body, tags=None):
        if tags is None:
            tags = []
        post_data = {"title": title, "body": body, "tags": tags}

        try:
            self._validate_post_data(post_data)

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
            formatted_post_data = self._format_post_data(post_data)
            return self._response(success=True, data=formatted_post_data)
        except ValidationError as e:
            return self._response(success=False, error=f"Validation error: {e.message}")
        except Exception as e:
            return self._response(success=False, error=str(e))

    def update_post(self, post_id, update_data):
        try:
            self._validate_post_data(update_data)

            update_data["updatedDate"] = datetime.now(timezone.utc).isoformat()
            expression = "SET " + ", ".join(f"{k}=:{k}" for k in update_data.keys())
            expression_values = {f":{k}": v for k, v in update_data.items()}

            self.table.update_item(
                Key={"id": post_id},
                UpdateExpression=expression,
                ExpressionAttributeValues=expression_values,
            )
            response = self.get_post_by_id(post_id)
            if response["success"]:
                formatted_post_data = self._format_post_data(response["data"])
                return self._response(success=True, data=formatted_post_data)
            else:
                return response
        except ValidationError as e:
            return self._response(success=False, error=f"Validation error: {e.message}")
        except Exception as e:
            return self._response(success=False, error=str(e))

    def delete_post(self, post_id):
        try:
            self.table.delete_item(Key={"id": post_id})
            return self._response(success=True, data="Post deleted successfully")
        except Exception as e:
            return self._response(success=False, error=str(e))
