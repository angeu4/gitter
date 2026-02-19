from pathlib import Path
import time

from gitter.objects.blob import Blob
from gitter.objects.tree import Tree
from gitter.objects.commit import Commit

from gitter.storage.hashing import sha1_hash
from gitter.storage.object_store import ObjectStore
from gitter.storage.serializer import serialize_dict, deserialize_dict
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

    def commit(self, message: str, author: str, auto_stage: bool = False):

        """
        Create commit from current index state.

        Returns:
            Commit hash.

        Raises:
            NothingToCommitError: If index is empty.
        """

        if auto_stage:
            self._auto_stage_tracked_changes()

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

    def _auto_stage_tracked_changes(self):
        """
        Stage modified and deleted tracked files.
        Does NOT stage untracked files.
        """

        index = self.index_store.load()

        # Load HEAD tree
        tracked = {}

        try:
            branch = self._get_current_branch_name()
            commit_hash = self.refs.get_branch(branch)

            if commit_hash:
                commit_path = self.layout.objects_dir / commit_hash
                commit_dict = deserialize_dict(commit_path.read_bytes())

                tree_hash = commit_dict["tree"]
                tree_path = self.layout.objects_dir / tree_hash
                tree_dict = deserialize_dict(tree_path.read_bytes())

                tracked = tree_dict.get("entries", {})
        except Exception:
            tracked = {}

        for path_str, blob_hash in tracked.items():
            path = self.repo_root / path_str

            # File deleted
            if not path.exists():
                index.entries[path_str] = None
                continue

            # File modified
            current_content = path.read_bytes()

            blob = Blob(current_content)
            new_hash = self.object_store.store(blob)

            if new_hash != blob_hash:
                index.entries[path_str] = new_hash

        self.index_store.save(index)


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

    # ------------------------------------------------------------------
    # Status
    # ------------------------------------------------------------------

    def get_status(self):
        """
        Compute repository status.

        Returns:
            dict with keys:
                - staged
                - modified
                - untracked
        """

        index = self.index_store.load()

        staged = set(index.entries.keys())
        modified = set()
        untracked = set()

        # Load HEAD tree if exists
        tracked = {}

        try:
            branch = self._get_current_branch_name()
            commit_hash = self.refs.get_branch(branch)

            if commit_hash:
                commit_data = self.object_store.objects_path / commit_hash
                commit_dict = deserialize_dict(commit_data.read_bytes())
                tree_hash = commit_dict["tree"]

                tree_data = self.object_store.objects_path / tree_hash
                tree_dict = deserialize_dict(tree_data.read_bytes())

                tracked = tree_dict.get("entries", {})
        except Exception:
            tracked = {}

        for path in self.repo_root.rglob("*"):
            if path.is_dir():
                continue

            if ".gitter" in path.parts:
                continue

            relative_path = str(path.relative_to(self.repo_root))

            current_content = path.read_bytes()

            blob_data = {
                "type": "blob",
                "content": current_content.decode("utf-8"),
            }
            blob_hash = sha1_hash(serialize_dict(blob_data))

            if relative_path in staged:
                if blob_hash != index.entries[relative_path]:
                    modified.add(relative_path)
            elif relative_path in tracked:
                if blob_hash != tracked[relative_path]:
                    modified.add(relative_path)
            else:
                untracked.add(relative_path)

        return {
            "staged": sorted(staged),
            "modified": sorted(modified),
            "untracked": sorted(untracked),
        }


    # ------------------------------------------------------------------
    # Log
    # ------------------------------------------------------------------

    def get_log(self):
        """
        Traverse commit history from HEAD backwards.

        Returns:
            List of commits in reverse chronological order.
            Each entry is a dict containing:
                - hash
                - message
                - author
                - timestamp
        """

        commits = []

        try:
            branch = self._get_current_branch_name()
            current_hash = self.refs.get_branch(branch)
        except Exception:
            return commits

        while current_hash:
            commit_path = self.layout.objects_dir / current_hash

            if not commit_path.exists():
                break

            commit_dict = deserialize_dict(commit_path.read_bytes())

            commits.append(
                {
                    "hash": current_hash,
                    "message": commit_dict["message"],
                    "author": commit_dict["author"],
                    "timestamp": commit_dict["timestamp"],
                }
            )

            current_hash = commit_dict.get("parent")

        return commits


    # ------------------------------------------------------------------
    # Branch
    # ------------------------------------------------------------------

    def list_branches(self):
        """
        Return list of branch names.
        """

        branches = []
        for path in self.layout.heads_dir.iterdir():
            if path.is_file():
                branches.append(path.name)

        return sorted(branches)


    def create_branch(self, name: str):
        """
        Create a new branch pointing to current HEAD commit.
        """

        branch_path = self.layout.heads_dir / name

        if branch_path.exists():
            raise ValueError("Branch already exists")

        current_branch = self._get_current_branch_name()
        current_commit = self.refs.get_branch(current_branch)

        self.refs.set_branch(name, current_commit)


    # ------------------------------------------------------------------
    # Reset
    # ------------------------------------------------------------------

    def reset_head(self, revision: str) -> str:
        """
        Reset current branch to HEAD~n.

        Only supports syntax: HEAD~<n>

        Returns:
            Target commit hash.

        Raises:
            ValueError if revision invalid or reset not possible.
        """

        if not revision.startswith("HEAD~"):
            raise ValueError("Invalid revision format")

        try:
            steps = int(revision.split("~")[1])
        except (IndexError, ValueError):
            raise ValueError("Invalid revision format")

        if steps <= 0:
            raise ValueError("Invalid revision format")

        branch_name = self._get_current_branch_name()
        current_hash = self.refs.get_branch(branch_name)

        if not current_hash:
            raise ValueError("No commits to reset")

        target_hash = current_hash

        for _ in range(steps):
            commit_path = self.layout.objects_dir / target_hash

            if not commit_path.exists():
                raise ValueError("Invalid commit history")

            commit_dict = deserialize_dict(commit_path.read_bytes())

            parent_hash = commit_dict.get("parent")

            if not parent_hash:
                raise ValueError("Cannot reset beyond initial commit")

            target_hash = parent_hash

        # Move branch reference
        self.refs.set_branch(branch_name, target_hash)

        return target_hash

    # ------------------------------------------------------------------
    # Checkout
    # ------------------------------------------------------------------

    def checkout_branch(self, name: str):
        """
        Switch HEAD to another branch and update working tree.

        Raises:
            ValueError if branch does not exist.
        """

        # Ensure branch exists
        branch_path = self.layout.heads_dir / name
        if not branch_path.exists():
            raise ValueError("Branch does not exist")

        # Get commit hash of target branch
        target_commit = self.refs.get_branch(name)

        # Update HEAD reference
        self.head.set_branch(name)

        # If branch has no commits yet, nothing to restore
        if not target_commit:
            return

        # Load commit
        commit_path = self.layout.objects_dir / target_commit
        commit_dict = deserialize_dict(commit_path.read_bytes())

        tree_hash = commit_dict["tree"]

        # Load tree
        tree_path = self.layout.objects_dir / tree_hash
        tree_dict = deserialize_dict(tree_path.read_bytes())

        entries = tree_dict.get("entries", {})

        # Clear working directory files (except .gitter)
        for path in self.repo_root.rglob("*"):
            if path.is_file() and ".gitter" not in path.parts:
                path.unlink()

        # Restore files from tree
        for path_str, blob_hash in entries.items():
            blob_path = self.layout.objects_dir / blob_hash
            blob_dict = deserialize_dict(blob_path.read_bytes())

            file_path = self.repo_root / path_str
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(blob_dict["content"])

        # Clear index after checkout
        self.index_store.save(Index())
