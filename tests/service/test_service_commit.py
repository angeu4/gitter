from pathlib import Path
import pytest

from gitter.service.repository_service import RepositoryService
from gitter.service.exceptions import NothingToCommitError


def _init_repo_structure(repo: Path):
    (repo / ".gitter").mkdir()
    (repo / ".gitter" / "objects").mkdir(parents=True)
    (repo / ".gitter" / "refs" / "heads").mkdir(parents=True)


def test_commit_empty_index_raises(tmp_path):
    repo = tmp_path
    _init_repo_structure(repo)

    service = RepositoryService(repo)

    with pytest.raises(NothingToCommitError):
        service.commit("msg", "author")


def test_commit_creates_commit_object(tmp_path):
    repo = tmp_path
    _init_repo_structure(repo)

    service = RepositoryService(repo)

    file = repo / "file.txt"
    file.write_text("hello")

    service.stage_file(file)

    commit_hash = service.commit("msg", "author")

    assert commit_hash is not None

    # index should be cleared
    index = service.index_store.load()
    assert index.entries == {}
