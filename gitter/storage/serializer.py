import json


def serialize_dict(data: dict) -> bytes:
    return json.dumps(data, sort_keys=True).encode()


def deserialize_dict(data: bytes) -> dict:
    return json.loads(data.decode())
