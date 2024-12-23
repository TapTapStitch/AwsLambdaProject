import boto3
import uuid
from datetime import datetime, timezone
from jsonschema import validate
from lambda_layer.decorators import exception_handler
from lambda_layer.schemas import post_schema


class PostService:
    def __init__(self, table_name="posts", region_name="eu-north-1"):
        self.dynamodb = boto3.resource("dynamodb", region_name=region_name)
        self.table = self.dynamodb.Table(table_name)

    def _validate_post_data(self, data):
        validate(instance=data, schema=post_schema())

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

    def _create_update_expression(self, update_data):
        update_data["updatedDate"] = datetime.now(timezone.utc).isoformat()
        expression = "SET " + ", ".join(f"{k}=:{k}" for k in update_data.keys())
        expression_values = {f":{k}": v for k, v in update_data.items()}
        return expression, expression_values

    @exception_handler
    def get_all_posts(self):
        response = self.table.scan()
        items = response.get("Items", [])
        formatted_items = [self._format_post_data(item) for item in items]
        return self._response(success=True, data=formatted_items)

    @exception_handler
    def get_post_by_id(self, post_id):
        response = self.table.get_item(Key={"id": post_id})
        item = response.get("Item", None)
        if item:
            formatted_item = self._format_post_data(item)
            return self._response(success=True, data=formatted_item)
        else:
            return self._response(success=False, error="Post not found")

    @exception_handler
    def create_post(self, title, body, tags=None):
        if tags is None:
            tags = []
        post_data = {"title": title, "body": body, "tags": tags}

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

    @exception_handler
    def update_post(self, post_id, update_data):
        self._validate_post_data(update_data)

        expression, expression_values = self._create_update_expression(update_data)

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

    @exception_handler
    def delete_post(self, post_id):
        self.table.delete_item(Key={"id": post_id})
        return self._response(success=True, data="Post deleted successfully")
