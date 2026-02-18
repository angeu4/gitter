import pytest

from gitter.repository.exceptions import HeadError
from gitter.repository.head import Head


def test_head_set_and_get(tmp_path):
    head_file = tmp_path / "HEAD"

    head = Head(head_file)
    head.set_branch("main")

    assert head.get_ref() == "ref: refs/heads/main"

def test_head_read_missing_file_raises(tmp_path):
    head = Head(tmp_path / "HEAD")

    with pytest.raises(HeadError):
        head.get_ref()
