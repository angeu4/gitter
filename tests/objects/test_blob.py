from gitter.objects.blob import Blob


def test_blob_roundtrip():
    blob = Blob(b"hello")
    data = blob.to_dict()
    new_blob = Blob.from_dict(data)
    assert new_blob.content == b"hello"
