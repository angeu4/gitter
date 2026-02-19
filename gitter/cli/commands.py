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
    """
    if "-m" not in args:
        return 1, "Usage: gitter commit -m <message>"

    msg_index = args.index("-m") + 1
    if msg_index >= len(args):
        return 1, "Commit message missing"

    message = args[msg_index]

    try:
        repo_root = find_repo_root(Path.cwd())
    except RepoNotFoundError:
        return 1, "Not a gitter repository"

    service = RepositoryService(repo_root)

    try:
        commit_hash = service.commit(message, "anonymous")
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
