from .base import GitterObject


class Tree(GitterObject):

    def __init__(self, entries: dict):
        self.entries = entries

    def to_dict(self):
        return {
            "type": "tree",
            "entries": self.entries,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["entries"])
