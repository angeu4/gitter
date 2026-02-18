from gitter.objects.tree import Tree


def test_tree_roundtrip():
    entries = {
        "app.py": "hash123",
        "utils.py": "hash456",
    }

    tree = Tree(entries)

    data = tree.to_dict()
    new_tree = Tree.from_dict(data)

    assert new_tree.entries == entries


def test_tree_empty_entries():
    tree = Tree({})
    assert tree.entries == {}
