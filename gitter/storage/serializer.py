import json
from .exceptions import SerializationError


def serialize_dict(data: dict) -> bytes:
    """
    Serialize dictionary into deterministic byte representation.

    Deterministic serialization is required to ensure identical objects
    always produce identical hashes.

    Args:
        data: JSON serializable dictionary.

    Returns:
        UTF-8 encoded JSON bytes with sorted keys.

    Raises:
        SerializationError: If data cannot be serialized.
    """
    try:
        return json.dumps(data, sort_keys=True).encode()
    except Exception as exc:
        raise SerializationError(str(exc)) from exc


def deserialize_dict(data: bytes) -> dict:
    """
    Deserialize bytes back into dictionary representation.

    Args:
        data: UTF-8 encoded JSON bytes.

    Returns:
        Parsed dictionary.

    Raises:
        SerializationError: If data cannot be decoded or parsed.
    """
    try:
        return json.loads(data.decode())
    except Exception as exc:
        raise SerializationError(str(exc)) from exc
