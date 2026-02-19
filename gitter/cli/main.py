import sys

from gitter.cli import commands


COMMAND_REGISTRY = {
    "init": {
        "handler": commands.init_command,
        "usage": "gitter init",
        "description": "Initialize a new repository",
    },
    "add": {
        "handler": commands.add_command,
        "usage": "gitter add <file>",
        "description": "Stage a file",
    },
    "commit": {
        "handler": commands.commit_command,
        "usage": "gitter commit -m <message>",
        "description": "Create a commit from staged files",
    },
    "status": {
        "handler": commands.status_command,
        "usage": "gitter status",
        "description": "Show repository status",
    },
    "log": {
        "handler": commands.log_command,
        "usage": "gitter log",
        "description": "Show commit history",
    },
    "branch": {
        "handler": commands.branch_command,
        "usage": "gitter branch [<name>]",
        "description": "List or create branches",
    },
    "reset": {
        "handler": commands.reset_command,
        "usage": "gitter reset HEAD~n",
        "description": "Reset to head revision",
    }
}


def print_global_help():
    print("Gitter CLI\n")
    print("Available commands:\n")
    for name, meta in COMMAND_REGISTRY.items():
        print(f"  {name:<10} {meta['description']}")
    print("\nRun 'gitter help <command>' for more information.")


def print_command_help(command):
    meta = COMMAND_REGISTRY.get(command)
    if not meta:
        print(f"Unknown command '{command}'")
        return 1

    print(meta["usage"])
    print()
    print(meta["description"])
    return 0


def main():
    args = sys.argv[1:]

    if not args:
        print_global_help()
        sys.exit(0)

    command = args[0]

    if command == "help":
        if len(args) == 1:
            print_global_help()
            sys.exit(0)
        else:
            exit_code = print_command_help(args[1])
            sys.exit(exit_code)

    meta = COMMAND_REGISTRY.get(command)

    if not meta:
        print(f"Unknown command '{command}'")
        sys.exit(1)

    handler = meta["handler"]

    exit_code, message = handler(args[1:])
    
    if message:
        print(message)
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
