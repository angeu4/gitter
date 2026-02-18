from .base import GitterObject


class Tree(GitterObject):
    """
    Represents directory snapshot mapping filenames to object hashes.

    entries format:
        { filename: object_hash }
    """

    def __init__(self, entries: dict):
        # Mapping of file/subtree name -> object hash
        self.entries = entries

    def to_dict(self):
        return {
            "type": "tree",
            "entries": self.entries,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["entries"])
