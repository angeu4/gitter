from gitter.storage.hashing import sha1_hash


def test_sha1_changes_with_input():
    assert sha1_hash(b"a") != sha1_hash(b"b")
