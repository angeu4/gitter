from pathlib import Path
from gitter.storage.serializer import serialize_dict, deserialize_dict
from .exceptions import IndexError, IndexCorruptedError
from .model import Index


class IndexStore:
    """
    Handles persistence of index file.
    """

    def __init__(self, index_file: Path):
        self.index_file = index_file

    def save(self, index: Index):
        """
        Persist index state to disk.
        """
        try:
            data = serialize_dict(index.to_dict())
            self.index_file.write_bytes(data)
        except Exception as exc:
            raise IndexError(str(exc)) from exc

    def load(self) -> Index:
        """
        Load index state from disk.

        Returns empty Index if file missing.
        """
        if not self.index_file.exists():
            return Index()

        try:
            raw = self.index_file.read_bytes()
            data = deserialize_dict(raw)
            return Index.from_dict(data)
        except Exception as exc:
            raise IndexCorruptedError(str(exc)) from exc
