from gitter.index.store import IndexStore
from gitter.index.model import Index


def test_save_and_load(tmp_path):
    index_file = tmp_path / "index"
    store = IndexStore(index_file)

    idx = Index()
    idx.add("file.txt", "abc123")

    store.save(idx)

    loaded = store.load()
    assert loaded.entries["file.txt"] == "abc123"


def test_load_missing_returns_empty(tmp_path):
    store = IndexStore(tmp_path / "index")
    idx = store.load()

    assert idx.entries == {}
