from pathlib import Path

from gitter.repository.layout import RepoLayout
from gitter.repository.discovery import find_repo_root, RepoNotFoundError
from gitter.repository.config import RepoConfig
from gitter.service.repository_service import RepositoryService
from gitter.service.exceptions import NothingToCommitError


def init_command(args):
    """
    Initialize a new Gitter repository.
    """
    layout = RepoLayout(Path.cwd())
    layout.ensure_exists()
    RepoConfig(layout.config_file).write_default()

    return 0, "Initialized empty Gitter repository"


def add_command(args):
    """
    Stage one or more files.
    Supports glob patterns.
    """

    if not args:
        return 1, "No file specified"

    try:
        repo_root = find_repo_root(Path.cwd())
    except RepoNotFoundError:
        return 1, "Not a gitter repository"

    service = RepositoryService(repo_root)

    staged_any = False

    for pattern in args:
        # Expand glob relative to repo root
        matches = list(repo_root.glob(pattern))

        for match in matches:
            if match.is_file():
                rel_path = match.relative_to(repo_root)
                service.stage_file(Path(str(rel_path)))
                staged_any = True

    # If nothing matched, do nothing (spec compliant)
    if not staged_any:
        return 0, ""

    return 0, ""


def commit_command(args):
    """
    Create commit from staged files.
    Supports -m and -am.
    """

    auto_stage = False
    messages = []

    i = 0
    while i < len(args):
        if args[i] == "-a":
            auto_stage = True
            i += 1
        elif args[i] == "-m":
            if i + 1 >= len(args):
                return 1, "Commit message missing"
            messages.append(args[i + 1])
            i += 2
        else:
            return 1, "Invalid commit arguments"

    if not messages:
        return 1, "Commit message missing"

    full_message = "\n\n".join(messages)

    try:
        repo_root = find_repo_root(Path.cwd())
    except RepoNotFoundError:
        return 1, "Not a gitter repository"

    service = RepositoryService(repo_root)

    try:
        commit_hash = service.commit(
            full_message,
            "user",
            auto_stage=auto_stage,
        )
    except NothingToCommitError:
        return 1, "Nothing to commit"

    return 0, f"Committed as {commit_hash}"


def status_command(args):
    """
    Display repository status with strict formatting compliance.
    """

    try:
        repo_root = find_repo_root(Path.cwd())
    except RepoNotFoundError:
        return 1, "Not a gitter repository"

    service = RepositoryService(repo_root)
    status = service.get_status()

    staged = status.get("staged", [])
    modified = status.get("modified", [])
    untracked = status.get("untracked", [])

    lines = []

    if staged:
        lines.append("Changes to be committed:")
        for path in staged:
            lines.append(f"  {path}")

    if modified:
        lines.append("Changes not staged for commit:")
        for path in modified:
            lines.append(f"  {path}")

    if untracked:
        lines.append("Untracked files:")
        for path in untracked:
            lines.append(f"  {path}")

    if not lines:
        return 0, "Working tree clean"

    return 0, "\n".join(lines)


def log_command(args):
    """
    Show commit history.
    """
    try:
        repo_root = find_repo_root(Path.cwd())
    except RepoNotFoundError:
        return 1, "Not a gitter repository"

    service = RepositoryService(repo_root)
    commits = service.get_log()

    if not commits:
        return 0, "No commits yet"

    lines = []

    for commit in commits:
        lines.append(f"commit {commit['hash']}")
        lines.append(f"Author: {commit['author']}")
        lines.append(f"Message: {commit['message']}")
        lines.append("")

    return 0, "\n".join(lines).strip()

def branch_command(args):
    """
    List or create branches.
    """

    try:
        repo_root = find_repo_root(Path.cwd())
    except RepoNotFoundError:
        return 1, "Not a gitter repository"

    service = RepositoryService(repo_root)

    # List branches
    if not args:
        branches = service.list_branches()
        current = service._get_current_branch_name()

        lines = []
        for branch in branches:
            prefix = "*" if branch == current else " "
            lines.append(f"{prefix} {branch}")

        return 0, "\n".join(lines)

    # Create branch
    name = args[0]

    try:
        service.create_branch(name)
    except ValueError:
        return 1, "Branch already exists"

    return 0, f"Branch '{name}' created"


def reset_command(args):
    if len(args) != 1:
        return 1, "Usage: gitter reset HEAD~<n>"

    revision = args[0]

    try:
        repo_root = find_repo_root(Path.cwd())
    except RepoNotFoundError:
        return 1, "Not a gitter repository"

    service = RepositoryService(repo_root)

    try:
        service.reset_head(revision)
    except ValueError as e:
        return 1, str(e)

    return 0, ""
