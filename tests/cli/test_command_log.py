from tests.cli.conftest import run_cli


def test_log_no_commits(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)

    run_cli(monkeypatch, ["init"])

    exit_code = run_cli(monkeypatch, ["log"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "No commits yet" in captured.out

def test_log_single_commit(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)

    run_cli(monkeypatch, ["init"])

    file = tmp_path / "file.txt"
    file.write_text("hello")

    run_cli(monkeypatch, ["add", "file.txt"])
    run_cli(monkeypatch, ["commit", "-m", "initial"])

    exit_code = run_cli(monkeypatch, ["log"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "commit" in captured.out
    assert "initial" in captured.out

def test_log_multiple_commits(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)

    run_cli(monkeypatch, ["init"])

    file = tmp_path / "file.txt"
    file.write_text("v1")

    run_cli(monkeypatch, ["add", "file.txt"])
    run_cli(monkeypatch, ["commit", "-m", "first"])

    file.write_text("v2")
    run_cli(monkeypatch, ["add", "file.txt"])
    run_cli(monkeypatch, ["commit", "-m", "second"])

    exit_code = run_cli(monkeypatch, ["log"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "second" in captured.out
    assert "first" in captured.out