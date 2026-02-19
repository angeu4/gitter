def test_global_help(monkeypatch, capsys, run_cli):
    exit_code = run_cli(monkeypatch, ["help"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Available commands" in captured.out


def test_command_help(monkeypatch, capsys, run_cli):
    exit_code = run_cli(monkeypatch, ["help", "commit"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "gitter commit -m <message>" in captured.out


def test_help_unknown_command(monkeypatch, capsys, run_cli):
    exit_code = run_cli(monkeypatch, ["help", "unknown"])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Unknown command" in captured.out