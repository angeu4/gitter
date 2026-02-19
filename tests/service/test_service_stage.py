from pathlib import Path
from gitter.service.repository_service import RepositoryService


def _init_repo_structure(repo: Path):
    (repo / ".gitter").mkdir()
    (repo / ".gitter" / "objects").mkdir(parents=True)
    (repo / ".gitter" / "refs" / "heads").mkdir(parents=True)


def test_stage_file_creates_index(tmp_path):
    repo = tmp_path
    _init_repo_structure(repo)

    service = RepositoryService(repo)

    file = repo / "file.txt"
    file.write_text("hello")

    service.stage_file(file)

    index_file = repo / ".gitter" / "index"
    assert index_file.exists()


def test_stage_stores_relative_path(tmp_path):
    repo = tmp_path
    _init_repo_structure(repo)

    service = RepositoryService(repo)

    file = repo / "nested.txt"
    file.write_text("data")

    service.stage_file(file)

    index = service.index_store.load()
    assert "nested.txt" in index.entries
