import re


def test_global_help(monkeypatch, capsys, run_cli):
    exit_code = run_cli(monkeypatch, ["help"])
    captured = capsys.readouterr()

    expected = (
        "Usage: gitter <command> [options]\n"
        "\n"
        "Available commands:\n"
        "  add\n"
        "  branch\n"
        "  checkout\n"
        "  commit\n"
        "  help\n"
        "  init\n"
        "  log\n"
        "  reset\n"
        "  status\n"
    )

    assert exit_code == 0
    assert captured.out == expected


def test_command_help(monkeypatch, capsys, run_cli):
    exit_code = run_cli(monkeypatch, ["help", "commit"])
    captured = capsys.readouterr()

    assert exit_code == 0

    expected = (
        "NAME:\n"
        "    gitter commit - Create a commit from staged files\n"
        "\n"
        "SYNOPSIS:\n"
        "    gitter commit -m <message> [-m <message>] [-a]\n"
        "\n"
        "DESCRIPTION:\n"
        "    Create a commit from staged files\n"
        "\n"
        "OPTIONS:\n"
        "    -m <message>   Commit message\n"
        "    -a             Auto stage tracked changes\n"
    )

    assert captured.out == expected



def test_help_unknown_command(monkeypatch, capsys, run_cli):
    exit_code = run_cli(monkeypatch, ["help", "unknown"])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert captured.out == "Unknown command\n"

def test_help_global_regex(monkeypatch, capsys, run_cli):
    exit_code = run_cli(monkeypatch, ["help"])
    captured = capsys.readouterr()

    assert exit_code == 0

    # At least one command line with: word + 2+ spaces + description
    pattern = r"(?m)^(?!These).*?(\w+)\s{2,}(.+)$"
    assert re.search(pattern, captured.out)

def test_help_commit_regex(monkeypatch, capsys, run_cli):
    exit_code = run_cli(monkeypatch, ["help", "commit"])
    captured = capsys.readouterr()

    assert exit_code == 0

    pattern = (
        r"(?s)"
        r"(NAME:)\s*.+?\n+"
        r"(SYNOPSIS:)\s*.+?\n+"
        r"(DESCRIPTION:)\s*.+?"
        r"(?:\n+(OPTIONS:)\s*.+)?$"
    )

    assert re.search(pattern, captured.out)
