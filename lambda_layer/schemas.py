def post_schema():
    schema = {
        "type": "object",
        "properties": {
            "title": {"type": "string", "minLength": 1, "maxLength": 200},
            "body": {"type": "string", "minLength": 1, "maxLength": 2000},
            "tags": {"type": "array", "items": {"type": "string"}},
        },
        "required": ["title", "body"],
        "additionalProperties": False,
    }
    return schema
