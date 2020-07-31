import typesystem
import json

from starlette.exceptions import HTTPException


async def validate(validator, request):
    try:
        json_data = await request.json()
    except json.decoder.JSONDecodeError:
        raise HTTPException(400, "Body is not JSON")
    data, errors = validator.validate_or_error(json_data)
    if errors:
        raise HTTPException(400, dict(errors))
    return dict(data)


string_pattern = "^[A-Za-z0-9-_]+$"
base64_pattern = "^[A-Za-z0-9/=+]+$"


class PushSerializer(typesystem.Schema):
    app_id = typesystem.String(max_length=36, pattern=string_pattern)
    username = typesystem.String(max_length=64, pattern=string_pattern)
    secret = typesystem.String(max_length=128, pattern=string_pattern)
    data_b64 = typesystem.String(max_length=4096, pattern=base64_pattern)


class SearchSerializer(typesystem.Schema):
    app_id = typesystem.String(max_length=36, pattern=string_pattern)
    username = typesystem.String(max_length=64, pattern=string_pattern)
    secret = typesystem.String(max_length=128, pattern=string_pattern)
