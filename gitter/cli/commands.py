from pathlib import Path

from gitter.repository.layout import RepoLayout
from gitter.repository.discovery import find_repo_root, RepoNotFoundError
from gitter.repository.config import RepoConfig
from gitter.service.repository_service import RepositoryService


def init_command(path: Path):
    """
    Initialize a new Gitter repository.
    """

    layout = RepoLayout(path)
    layout.ensure_exists()

    RepoConfig(layout.config_file).write_default()

    return "Initialized empty Gitter repository"


def add_command(file_path: str):
    """
    Stage a file into the repository.
    """

    try:
        repo_root = find_repo_root(Path.cwd())
    except RepoNotFoundError:
        raise RuntimeError("Not a gitter repository")

    service = RepositoryService(repo_root)

    service.stage_file(Path(file_path))

    return f"Staged {file_path}"


def commit_command(message: str, author: str = "anonymous"):
    """
    Create commit from staged files.
    """

    try:
        repo_root = find_repo_root(Path.cwd())
    except RepoNotFoundError:
        raise RuntimeError("Not a gitter repository")

    service = RepositoryService(repo_root)

    commit_hash = service.commit(message, author)

    return f"Committed as {commit_hash}"
