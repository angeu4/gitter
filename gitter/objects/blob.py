from .base import GitterObject


class Blob(GitterObject):

    def __init__(self, content: bytes):
        self.content = content

    def to_dict(self):
        return {
            "type": "blob",
            "content": self.content.decode("utf-8"),
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["content"].encode())
