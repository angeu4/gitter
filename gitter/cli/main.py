import sys


def main():
    if len(sys.argv) == 1:
        print("Gitter CLI - run 'gitter help'")
        return

    command = sys.argv[1]
    print(f"Command '{command}' not implemented yet")
