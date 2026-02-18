from .exceptions import RefError, RefNotFoundError


class Refs:
    """
    Manages branch reference files.

    Each branch is stored as file containing latest commit hash.
    """

    def __init__(self, heads_dir):
        self.heads_dir = heads_dir

    def set_branch(self, name: str, commit_hash: str):
        """
        Update branch pointer.

        Raises:
            RefError: If filesystem write fails.
        """
        try:
            path = self.heads_dir / name
            path.write_text(commit_hash)
        except OSError as exc:
            raise RefError(str(exc)) from exc
    
    def get_branch(self, name: str) -> str:
        """
        Retrieve commit hash for branch.

        Raises:
            RefNotFoundError: If branch does not exist.
            RefError: If filesystem read fails.
        """
        path = self.heads_dir / name

        try:
            if not path.exists():
                raise RefNotFoundError(f"Branch '{name}' not found")

            return path.read_text().strip()

        except OSError as exc:
            raise RefError(str(exc)) from exc

