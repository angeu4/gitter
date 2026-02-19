class Index:
    """
    Represents staging area state.

    Maintains mapping of file path -> blob hash.
    """

    def __init__(self, entries: dict | None = None):
        # Deterministic ordering important for stable serialization
        self.entries = entries or {}

    def add(self, path: str, blob_hash: str):
        """
        Stage file with corresponding blob hash.
        """
        self.entries[path] = blob_hash

    def remove(self, path: str):
        """
        Remove file from staging area.
        """
        self.entries.pop(path, None)

    def to_dict(self) -> dict:
        """
        Return deterministic dictionary representation.
        """
        return {"entries": dict(sorted(self.entries.items()))}

    @classmethod
    def from_dict(cls, data: dict):
        return cls(entries=data.get("entries", {}))
