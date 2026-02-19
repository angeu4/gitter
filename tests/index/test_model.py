from gitter.index.model import Index


def test_add_and_remove():
    idx = Index()

    idx.add("file.txt", "abc123")
    assert idx.entries["file.txt"] == "abc123"

    idx.remove("file.txt")
    assert "file.txt" not in idx.entries


def test_deterministic_order():
    idx = Index()
    idx.add("b.txt", "2")
    idx.add("a.txt", "1")

    data = idx.to_dict()
    assert list(data["entries"].keys()) == ["a.txt", "b.txt"]
