import sys
from pathlib import Path

from gitter.cli.commands import (
    init_command,
    add_command,
    commit_command,
)
from gitter.service.exceptions import NothingToCommitError


def main():
    """
    Entry point for Gitter CLI.
    """

    args = sys.argv[1:]

    if not args:
        print("Gitter CLI")
        sys.exit(0)

    command = args[0]

    try:
        if command == "init":
            print(init_command(Path.cwd()))
            sys.exit(0)

        elif command == "add":
            if len(args) < 2:
                print("Usage: gitter add <file>")
                sys.exit(1)

            print(add_command(args[1]))
            sys.exit(0)

        elif command == "commit":
            if "-m" not in args:
                print("Usage: gitter commit -m <message>")
                sys.exit(1)

            msg_index = args.index("-m") + 1

            if msg_index >= len(args):
                print("Commit message missing")
                sys.exit(1)

            message = args[msg_index]

            print(commit_command(message))
            sys.exit(0)

        else:
            print(f"Unknown command '{command}'")
            sys.exit(1)

    except NothingToCommitError:
        print("Nothing to commit")
        sys.exit(1)

    except FileNotFoundError as exc:
        print(f"File not found: {exc}")
        sys.exit(1)

    except RuntimeError as exc:
        print(str(exc))
        sys.exit(1)

    except Exception as exc:
        # Catch-all for unexpected failures
        print(f"Unexpected error: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
