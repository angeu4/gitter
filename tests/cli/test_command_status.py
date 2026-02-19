def test_status_untracked(tmp_path, monkeypatch, capsys, run_cli):
    monkeypatch.chdir(tmp_path)

    run_cli(monkeypatch, ["init"])

    file = tmp_path / "file.txt"
    file.write_text("hello")

    exit_code = run_cli(monkeypatch, ["status"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Untracked" in captured.out
    assert "file.txt" in captured.out

def test_status_staged(tmp_path, monkeypatch, capsys, run_cli):
    monkeypatch.chdir(tmp_path)

    run_cli(monkeypatch, ["init"])

    file = tmp_path / "file.txt"
    file.write_text("hello")

    run_cli(monkeypatch, ["add", "file.txt"])

    exit_code = run_cli(monkeypatch, ["status"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Staged" in captured.out

def test_status_clean(tmp_path, monkeypatch, capsys, run_cli):
    monkeypatch.chdir(tmp_path)

    run_cli(monkeypatch, ["init"])

    file = tmp_path / "file.txt"
    file.write_text("hello")

    run_cli(monkeypatch, ["add", "file.txt"])
    run_cli(monkeypatch, ["commit", "-m", "msg"])

    exit_code = run_cli(monkeypatch, ["status"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Working tree clean" in captured.out