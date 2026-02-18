import pytest

from gitter.repository.discovery import find_repo_root, RepoNotFoundError


def test_find_repo_root(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()

    (repo / ".gitter").mkdir()

    sub = repo / "sub"
    sub.mkdir()

    assert find_repo_root(sub) == repo


def test_repo_not_found(tmp_path):
    with pytest.raises(RepoNotFoundError):
        find_repo_root(tmp_path)
