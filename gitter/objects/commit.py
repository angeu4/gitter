from .base import GitterObject


class Commit(GitterObject):
    """
    Represents repository snapshot metadata.

    Stores:
    - Root tree hash
    - Parent commit reference
    - Author metadata
    - Timestamp
    - Commit message
    """

    def __init__(self, tree_hash, parent_hash, message, author, timestamp):
        self.tree_hash = tree_hash
        self.parent_hash = parent_hash
        self.message = message
        self.author = author
        self.timestamp = timestamp

    def to_dict(self):
        return {
            "type": "commit",
            "tree": self.tree_hash,
            "parent": self.parent_hash,
            "message": self.message,
            "author": self.author,
            "timestamp": self.timestamp,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["tree"],
            data.get("parent"),
            data["message"],
            data["author"],
            data["timestamp"],
        )
