class StorageError(Exception):
    """Base exception for storage layer."""


class SerializationError(StorageError):
    """Serialization or deserialization failed."""


class ObjectStoreError(StorageError):
    """Object store persistence failure."""
