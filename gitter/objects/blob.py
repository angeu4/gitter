from .base import GitterObject


class Blob(GitterObject):
    """
    Represents raw file content snapshot.

    Blob contains ONLY file bytes. No filename or metadata.
    """

    def __init__(self, content: bytes):
        # Raw file content stored as immutable bytes
        self.content = content

    def to_dict(self):
        return {
            "type": "blob",
            # Stored as UTF-8 string for JSON serialization
            "content": self.content.decode("utf-8"),
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["content"].encode())
