def test_reset_head(tmp_path, monkeypatch, capsys, run_cli):
    monkeypatch.chdir(tmp_path)

    run_cli(monkeypatch, ["init"])
    capsys.readouterr()

    file = tmp_path / "file.txt"

    file.write_text("v1")
    run_cli(monkeypatch, ["add", "file.txt"])
    run_cli(monkeypatch, ["commit", "-m", "first"])
    capsys.readouterr()

    file.write_text("v2")
    run_cli(monkeypatch, ["add", "file.txt"])
    run_cli(monkeypatch, ["commit", "-m", "second"])
    capsys.readouterr()

    exit_code = run_cli(monkeypatch, ["reset", "HEAD~1"])
    capsys.readouterr()

    assert exit_code == 0

    exit_code = run_cli(monkeypatch, ["log"])
    captured = capsys.readouterr()

    assert "second" not in captured.out
    assert "first" in captured.out

def test_reset_invalid_format(tmp_path, monkeypatch, run_cli):
    monkeypatch.chdir(tmp_path)

    run_cli(monkeypatch, ["init"])

    exit_code = run_cli(monkeypatch, ["reset", "INVALID"])
    assert exit_code == 1

def test_reset_beyond_initial(tmp_path, monkeypatch, run_cli):
    monkeypatch.chdir(tmp_path)

    run_cli(monkeypatch, ["init"])

    file = tmp_path / "file.txt"
    file.write_text("v1")
    run_cli(monkeypatch, ["add", "file.txt"])
    run_cli(monkeypatch, ["commit", "-m", "first"])

    exit_code = run_cli(monkeypatch, ["reset", "HEAD~1"])
    assert exit_code == 1
