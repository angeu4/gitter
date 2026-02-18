from pathlib import Path

import pytest

from gitter.storage.exceptions import ObjectStoreError
from gitter.objects.blob import Blob
from gitter.storage.object_store import ObjectStore


def test_store_blob(tmp_path: Path):
    store = ObjectStore(tmp_path)
    blob = Blob(b"hello")

    object_hash = store.store(blob)

    stored_file = tmp_path / object_hash
    assert stored_file.exists()

def test_store_same_object_same_hash(tmp_path):
    store = ObjectStore(tmp_path)

    blob1 = Blob(b"hello")
    blob2 = Blob(b"hello")

    assert store.store(blob1) == store.store(blob2)

def test_object_store_wraps_os_error(tmp_path):
    store = ObjectStore(tmp_path)

    store.objects_path.chmod(0o400)

    with pytest.raises(ObjectStoreError):
        store.store(Blob(b"hello"))
