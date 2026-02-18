from pathlib import Path

from .hashing import sha1_hash
from .serializer import serialize_dict


class ObjectStore:

    def __init__(self, objects_path: Path):
        self.objects_path = objects_path

    def store(self, obj):
        data_bytes = serialize_dict(obj.to_dict())
        object_hash = sha1_hash(data_bytes)

        object_path = self.objects_path / object_hash
        object_path.write_bytes(data_bytes)

        return object_hash
