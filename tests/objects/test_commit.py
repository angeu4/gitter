from gitter.objects.commit import Commit


def test_commit_roundtrip():
    commit = Commit(
        tree_hash="tree123",
        parent_hash="parent123",
        message="msg",
        author="user",
        timestamp=123456,
    )

    data = commit.to_dict()
    new_commit = Commit.from_dict(data)

    assert new_commit.tree_hash == "tree123"
    assert new_commit.parent_hash == "parent123"


def test_commit_optional_parent():
    commit = Commit(
        tree_hash="tree123",
        parent_hash=None,
        message="msg",
        author="user",
        timestamp=123456,
    )

    data = commit.to_dict()
    new_commit = Commit.from_dict(data)

    assert new_commit.parent_hash is None
