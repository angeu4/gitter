from pathlib import Path

from .exceptions import ObjectStoreError
from .hashing import sha1_hash
from .serializer import serialize_dict


class ObjectStore:
    """
    Filesystem-backed content-addressable object storage.

    Responsible only for:
    - Serializing objects
    - Hashing serialized content
    - Persisting object bytes to disk

    Does NOT:
    - Understand repository state
    - Handle object relationships
    - Perform object validation beyond serialization

    Objects are stored using SHA1(content) as filename.
    """

    def __init__(self, objects_path: Path):
        """
        Initialize object store with base objects directory.

        Args:
            objects_path: Path to .gitter/objects directory.
        """
        self.objects_path = objects_path

    def store(self, obj):
        """
        Persist object and return content hash.

        Args:
            obj: GitterObject implementing to_dict().

        Returns:
            SHA1 hash identifying stored object.

        Raises:
            ObjectStoreError: If filesystem write fails.
        """
        data_bytes = serialize_dict(obj.to_dict())
        object_hash = sha1_hash(data_bytes)

        object_path = self.objects_path / object_hash

        try:
            object_path.write_bytes(data_bytes)
        except OSError as exc:
            raise ObjectStoreError(str(exc)) from exc

        return object_hash
