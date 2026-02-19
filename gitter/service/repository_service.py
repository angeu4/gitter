from pathlib import Path
import time

from gitter.objects.blob import Blob
from gitter.objects.tree import Tree
from gitter.objects.commit import Commit

from gitter.storage.object_store import ObjectStore
from gitter.repository.layout import RepoLayout
from gitter.repository.refs import Refs
from gitter.repository.head import Head
from gitter.repository.exceptions import RefNotFoundError, HeadError
from gitter.index.store import IndexStore
from gitter.index.model import Index

from .exceptions import NothingToCommitError


class RepositoryService:
    """
    Orchestrates repository operations using lower-level primitives.

    Coordinates:
        - Object storage
        - Index state
        - Repository metadata (HEAD + refs)

    Does NOT:
        - Handle CLI input/output
        - Print messages
        - Perform diff/status logic
    """

    DEFAULT_BRANCH = "main"

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root.resolve()

        self.layout = RepoLayout(self.repo_root)
        self.layout.ensure_exists()

        self.object_store = ObjectStore(self.layout.objects_dir)
        self.index_store = IndexStore(self.layout.gitter_dir / "index")
        self.refs = Refs(self.layout.heads_dir)
        self.head = Head(self.layout.head_file)

        self._ensure_repository_initialized()

    # ------------------------------------------------------------------
    # Repository Initialization Safety
    # ------------------------------------------------------------------

    def _ensure_repository_initialized(self):
        """
        Ensure HEAD and default branch are initialized.

        If HEAD does not exist:
            - Create default branch reference
            - Point HEAD to default branch
        """
        try:
            self.head.get_ref()
        except HeadError:
            # Initialize default branch with no commit yet
            self.refs.set_branch(self.DEFAULT_BRANCH, "")
            self.head.set_branch(self.DEFAULT_BRANCH)

    # ------------------------------------------------------------------
    # Stage (Add)
    # ------------------------------------------------------------------

    def stage_file(self, file_path: Path):
        """
        Stage a file into the index.

        Steps:
            - Read file content
            - Create Blob
            - Store Blob
            - Update Index with relative path
        """

        file_path = file_path.resolve()

        if not file_path.exists():
            raise FileNotFoundError(str(file_path))

        # Store relative path only
        relative_path = file_path.relative_to(self.repo_root)

        content = file_path.read_bytes()

        blob = Blob(content)
        blob_hash = self.object_store.store(blob)

        index = self.index_store.load()
        index.add(str(relative_path), blob_hash)
        self.index_store.save(index)

    # ------------------------------------------------------------------
    # Commit
    # ------------------------------------------------------------------

    def commit(self, message: str, author: str) -> str:
        """
        Create commit from current index state.

        Returns:
            Commit hash.

        Raises:
            NothingToCommitError: If index is empty.
        """

        index = self.index_store.load()

        if not index.entries:
            raise NothingToCommitError()

        # Build tree object from staged entries
        tree = Tree(index.entries)
        tree_hash = self.object_store.store(tree)

        # Determine parent commit (if any)
        branch_name = self._get_current_branch_name()

        try:
            parent_hash = self.refs.get_branch(branch_name)
            if parent_hash == "":
                parent_hash = None
        except RefNotFoundError:
            parent_hash = None

        commit = Commit(
            tree_hash=tree_hash,
            parent_hash=parent_hash,
            message=message,
            author=author,
            timestamp=int(time.time()),
        )

        commit_hash = self.object_store.store(commit)

        # Update branch to new commit
        self.refs.set_branch(branch_name, commit_hash)

        # Clear index after successful commit
        self.index_store.save(Index())

        return commit_hash

    # ------------------------------------------------------------------
    # Internal Helpers
    # ------------------------------------------------------------------

    def _get_current_branch_name(self) -> str:
        """
        Extract current branch name from HEAD.
        """

        ref = self.head.get_ref()

        # Expected format: ref: refs/heads/<branch>
        if not ref.startswith("ref: refs/heads/"):
            raise HeadError("Invalid HEAD format")

        return ref.split("/")[-1]
