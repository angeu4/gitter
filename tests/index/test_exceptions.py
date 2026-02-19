import pytest
from gitter.index.store import IndexStore
from gitter.index.exceptions import IndexCorruptedError


def test_load_corrupted_index(tmp_path):
    index_file = tmp_path / "index"
    index_file.write_text("invalid json")

    store = IndexStore(index_file)

    with pytest.raises(IndexCorruptedError):
        store.load()
