from datetime import datetime
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

    repo_root = Path.cwd()
    layout = RepoLayout(repo_root)
    gitter_dir = layout.gitter_dir

    if gitter_dir.exists():
        path_str = str(gitter_dir.resolve()) + "/"
        return 0, f"Gitter repository is already initialised in {path_str}"

    # Create directory structure
    layout.ensure_exists()

    # Create default config
    RepoConfig(layout.config_file).write_default()

    path_str = str(gitter_dir.resolve()) + "/"
    return 0, f"Initialized empty Gitter repository in {path_str}"


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
    Display repository status in strict format.
    """

    try:
        repo_root = find_repo_root(Path.cwd())
    except RepoNotFoundError:
        return 1, "Not a gitter repository"

    service = RepositoryService(repo_root)
    status = service.get_status()

    staged = status["staged"]
    modified = status["modified"]
    untracked = status["untracked"]

    lines = []

    if not staged and not modified and not untracked:
        return 0, "Working tree clean"

    # -------------------------
    # Staged
    # -------------------------
    if staged:
        lines.append("Changes to be committed:")
        for file in staged:
            lines.append(f"    new file: {file}")
        if modified or untracked:
            lines.append("")

    # -------------------------
    # Modified
    # -------------------------
    if modified:
        lines.append("Changes not staged for commit:")
        for file in modified:
            lines.append(f"    modified: {file}")
        if untracked:
            lines.append("")

    # -------------------------
    # Untracked
    # -------------------------
    if untracked:
        lines.append("Untracked files:")
        for file in untracked:
            lines.append(f"    {file}")

    if not lines:
        return 0, "Working tree clean"

    return 0, "\n".join(lines)



def log_command(args):
    """
    Display commit history in strict format compliance.
    """

    try:
        repo_root = find_repo_root(Path.cwd())
    except RepoNotFoundError:
        return 1, "Not a gitter repository"

    service = RepositoryService(repo_root)
    commits = service.get_log()

    if not commits:
        return 0, ""

    lines = []

    for commit in commits:
        commit_hash = commit["hash"]
        author = commit["author"]
        timestamp = commit["timestamp"]
        message = commit["message"]

        formatted_date = datetime.fromtimestamp(timestamp).strftime(
            "%a %b %d %H:%M:%S %Y"
        )

        lines.append(f"commit {commit_hash}")
        lines.append(f"Author: {author}")
        lines.append(f"Date:   {formatted_date}")
        lines.append("")
        lines.append(f"    {message}")

        # Separate commits with blank line (except last)
        if commit != commits[-1]:
            lines.append("")

    return 0, "\n".join(lines)


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


def help_command(args):
    """
    Display help information with strict formatting compliance.
    """

    command_meta = {
        "init": {
            "description": "Initialize a new repository",
            "usage": "gitter init",
        },
        "add": {
            "description": "Stage files",
            "usage": "gitter add <file|pattern>",
        },
        "commit": {
            "description": "Create a commit from staged files",
            "usage": "gitter commit -m <message> [-m <message>] [-a]",
            "options": [
                "-m <message>   Commit message",
                "-a             Auto stage tracked changes",
            ],
        },
        "status": {
            "description": "Show repository status",
            "usage": "gitter status",
        },
        "log": {
            "description": "Show commit history",
            "usage": "gitter log",
        },
        "branch": {
            "description": "List or create branches",
            "usage": "gitter branch [<name>]",
        },
        "reset": {
            "description": "Reset to previous revision",
            "usage": "gitter reset HEAD~<n>",
        },
        "checkout": {
            "description": "Switch branches",
            "usage": "gitter checkout <branch>",
        },
        "help": {
            "description": "Show help information",
            "usage": "gitter help [command]",
        },
    }

    # ------------------------------------------------------------------
    # Global help
    # ------------------------------------------------------------------

    if not args:
        lines = [
            "Usage: gitter <command> [options]",
            "",
            "Available commands:",
        ]

        for name in sorted(command_meta.keys()):
            lines.append(f"  {name}")

        return 0, "\n".join(lines)

    # ------------------------------------------------------------------
    # Command-specific help
    # ------------------------------------------------------------------

    command = args[0]

    if command not in command_meta:
        return 1, "Unknown command"

    meta = command_meta[command]

    lines = []

    lines.append("NAME:")
    lines.append(f"    gitter {command} - {meta['description']}")
    lines.append("")

    lines.append("SYNOPSIS:")
    lines.append(f"    {meta['usage']}")
    lines.append("")

    lines.append("DESCRIPTION:")
    lines.append(f"    {meta['description']}")

    if "options" in meta:
        lines.append("")
        lines.append("OPTIONS:")
        for opt in meta["options"]:
            lines.append(f"    {opt}")

    return 0, "\n".join(lines)


def checkout_command(args):

    return -1, ""