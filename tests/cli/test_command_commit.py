import re


def test_commit_without_staging(tmp_path, monkeypatch, capsys, run_cli):
    monkeypatch.chdir(tmp_path)

    run_cli(monkeypatch, ["init"])

    exit_code = run_cli(monkeypatch, ["commit", "-m", "msg"])

    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Nothing to commit" in captured.out

def test_missing_commit_message(monkeypatch, capsys, run_cli):
    exit_code = run_cli(monkeypatch, ["commit"])

    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Commit message missing" in captured.out

def test_full_add_and_commit_flow(tmp_path, monkeypatch, capsys, run_cli):
    monkeypatch.chdir(tmp_path)

    # init
    run_cli(monkeypatch, ["init"])

    # create file
    file = tmp_path / "file.txt"
    file.write_text("hello")

    # add
    exit_code = run_cli(monkeypatch, ["add", "file.txt"])
    assert exit_code == 0

    # commit
    exit_code = run_cli(monkeypatch, ["commit", "-m", "initial"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Committed as" in captured.out

def test_commit_status_regex(monkeypatch, capsys, run_cli, tmp_path):
    monkeypatch.chdir(tmp_path)

    run_cli(monkeypatch, ["init"])
    capsys.readouterr()

    (tmp_path / "file.txt").write_text("x")

    run_cli(monkeypatch, ["add", "*.txt"])
    capsys.readouterr()

    run_cli(monkeypatch, ["commit", "-m", "adds file"])
    capsys.readouterr()

    _ = run_cli(monkeypatch, ["status"])
    captured = capsys.readouterr()

    assert captured.out == "Working tree clean\n"


def test_commit_success_regex(monkeypatch, capsys, run_cli, tmp_path):
    monkeypatch.chdir(tmp_path)

    run_cli(monkeypatch, ["init"])
    capsys.readouterr()

    (tmp_path / "file.txt").write_text("x")
    run_cli(monkeypatch, ["add", "file.txt"])
    capsys.readouterr()

    exit_code = run_cli(monkeypatch, ["commit", "-m", "initial commit"])
    captured = capsys.readouterr()

    assert exit_code == 0

    pattern = r"^Committed as [a-f0-9]{40}\n$"
    assert re.fullmatch(pattern, captured.out)


def test_commit_missing_message_regex(monkeypatch, capsys, run_cli):
    exit_code = run_cli(monkeypatch, ["commit"])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert re.fullmatch(r"Commit message missing\n", captured.out)
