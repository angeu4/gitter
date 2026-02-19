import sys
from gitter.cli import commands


COMMAND_REGISTRY = {
    "init": {"handler": commands.init_command},
    "add": {"handler": commands.add_command},
    "commit": {"handler": commands.commit_command},
    "status": {"handler": commands.status_command},
    "log": {"handler": commands.log_command},
    "branch": {"handler": commands.branch_command},
    "reset": {"handler": commands.reset_command},
    "checkout": {"handler": commands.checkout_command},
    "help": {"handler": commands.help_command},
}


def main():
    args = sys.argv[1:]

    # No args → print banner + help
    if not args:
        print("Gitter CLI\n")
        exit_code, message = commands.help_command([])
        if message:
            print(message)
        sys.exit(exit_code)

    command = args[0]
    meta = COMMAND_REGISTRY.get(command)

    if not meta:
        print(f"Unknown command {command}")
        sys.exit(1)

    handler = meta["handler"]
    exit_code, message = handler(args[1:])

    if message:
        print(message)

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
