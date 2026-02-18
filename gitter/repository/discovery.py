from pathlib import Path


class RepoNotFoundError(Exception):
    """
    Raised when repository root cannot be located from given path.
    """
    pass


def find_repo_root(start: Path) -> Path:
    """
    Locate repository root by walking upward looking for .gitter directory.

    Args:
        start: Starting filesystem path.

    Returns:
        Repository root path.

    Raises:
        RepoNotFoundError: If repository not found.
    """
    current = start.resolve()

    while True:
        if (current / ".gitter").exists():
            return current

        if current.parent == current:
            raise RepoNotFoundError()

        current = current.parent
