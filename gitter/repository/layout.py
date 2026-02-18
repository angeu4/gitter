from pathlib import Path

from .exceptions import RepositoryError



class RepoLayout:
    """
    Defines canonical filesystem layout for a Gitter repository.

    Responsible only for computing paths and creating directory structure.
    Does NOT manage repository state or object logic.
    """

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.gitter_dir = repo_root / ".gitter"

        self.objects_dir = self.gitter_dir / "objects"
        self.refs_dir = self.gitter_dir / "refs"
        self.heads_dir = self.refs_dir / "heads"

        self.head_file = self.gitter_dir / "HEAD"
        self.config_file = self.gitter_dir / "config"

    def ensure_exists(self):
        """
        Create required repository directory structure.

        Raises:
            RepositoryError: If filesystem directory creation fails.
        """
        try:
            self.objects_dir.mkdir(parents=True, exist_ok=True)
            self.heads_dir.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            raise RepositoryError(str(exc)) from exc

