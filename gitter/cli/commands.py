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
    Stage a file into the repository.
    """
    if len(args) < 1:
        return 1, "Usage: gitter add <file>"

    try:
        repo_root = find_repo_root(Path.cwd())
    except RepoNotFoundError:
        return 1, "Not a gitter repository"

    service = RepositoryService(repo_root)

    try:
        service.stage_file(Path(args[0]))
    except FileNotFoundError as exc:
        return 1, f"File not found: {exc}"

    return 0, f"Staged {args[0]}"


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
    Show repository status.
    """
    try:
        repo_root = find_repo_root(Path.cwd())
    except RepoNotFoundError:
        return 1, "Not a gitter repository"

    service = RepositoryService(repo_root)
    status = service.get_status()

    output_lines = []

    if status["staged"]:
        output_lines.append("Staged:")
        output_lines.extend(f"  {f}" for f in status["staged"])

    if status["modified"]:
        output_lines.append("Modified:")
        output_lines.extend(f"  {f}" for f in status["modified"])

    if status["untracked"]:
        output_lines.append("Untracked:")
        output_lines.extend(f"  {f}" for f in status["untracked"])

    if not output_lines:
        output_lines.append("Working tree clean")

    return 0, "\n".join(output_lines)


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
