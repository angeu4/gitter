def test_unknown_command(monkeypatch, capsys, run_cli):
    exit_code = run_cli(monkeypatch, ["unknown"])

    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Unknown command" in captured.out

def test_no_args_prints_banner(monkeypatch, capsys, run_cli):
    exit_code = run_cli(monkeypatch, [])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Gitter CLI" in captured.out