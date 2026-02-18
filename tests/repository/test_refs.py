import pytest

from gitter.repository.exceptions import RefNotFoundError
from gitter.repository.refs import Refs


def test_set_and_get_branch(tmp_path):
    refs = Refs(tmp_path)

    refs.set_branch("main", "abc123")

    assert refs.get_branch("main") == "abc123"

def test_get_missing_branch_raises(tmp_path):
    refs = Refs(tmp_path)

    with pytest.raises(RefNotFoundError):
        refs.get_branch("main")
