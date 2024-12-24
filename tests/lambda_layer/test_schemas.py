from lambda_layer.schemas import post_schema


def test_post_schema_structure():
    schema = post_schema()
    expected_schema = {
        "type": "object",
        "properties": {
            "title": {"type": "string", "minLength": 1, "maxLength": 200},
            "body": {"type": "string", "minLength": 1, "maxLength": 2000},
            "tags": {"type": "array", "items": {"type": "string"}},
        },
        "required": ["title", "body"],
        "additionalProperties": False,
    }

    assert schema == expected_schema
