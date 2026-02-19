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
    assert captured.out == "Usage: gitter commit -m <message> [-m <message>] [-a]\n"


def test_help_unknown_command(monkeypatch, capsys, run_cli):
    exit_code = run_cli(monkeypatch, ["help", "unknown"])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert captured.out == "Unknown command\n"
