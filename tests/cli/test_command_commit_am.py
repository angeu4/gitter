import re


def test_commit_am_stages_modified(tmp_path, monkeypatch, capsys, run_cli):
    monkeypatch.chdir(tmp_path)

    run_cli(monkeypatch, ["init"])

    file = tmp_path / "file.txt"
    file.write_text("v1")

    run_cli(monkeypatch, ["add", "file.txt"])
    run_cli(monkeypatch, ["commit", "-m", "first"])

    file.write_text("v2")

    exit_code = run_cli(monkeypatch, ["commit", "-a", "-m", "second"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Committed as" in captured.out

def test_commit_am_does_not_stage_untracked(tmp_path, monkeypatch, capsys, run_cli):
    monkeypatch.chdir(tmp_path)

    run_cli(monkeypatch, ["init"])

    file = tmp_path / "file.txt"
    file.write_text("v1")

    exit_code = run_cli(monkeypatch, ["commit", "-a", "-m", "msg"])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Nothing to commit" in captured.out

def test_commit_multiple_m(tmp_path, monkeypatch, capsys, run_cli):
    monkeypatch.chdir(tmp_path)

    run_cli(monkeypatch, ["init"])

    file = tmp_path / "file.txt"
    file.write_text("v1")

    run_cli(monkeypatch, ["add", "file.txt"])

    run_cli(monkeypatch, ["commit", "-m", "line1", "-m", "line2"])

    _ = run_cli(monkeypatch, ["log"])
    captured = capsys.readouterr()

    assert "line1" in captured.out
    assert "line2" in captured.out


def test_commit_am_regex(monkeypatch, capsys, run_cli, tmp_path):
    monkeypatch.chdir(tmp_path)

    run_cli(monkeypatch, ["init"])
    capsys.readouterr()

    (tmp_path / "file.txt").write_text("v1")
    run_cli(monkeypatch, ["add", "file.txt"])
    run_cli(monkeypatch, ["commit", "-m", "first"])
    capsys.readouterr()

    (tmp_path / "file.txt").write_text("v2")

    exit_code = run_cli(monkeypatch, ["commit", "-am", "update"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert re.fullmatch(r"Committed as [a-f0-9]{40}\n", captured.out)
