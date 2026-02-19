from tests.cli.conftest import run_cli


def test_commit_without_staging(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)

    run_cli(monkeypatch, ["init"])

    exit_code = run_cli(monkeypatch, ["commit", "-m", "msg"])

    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Nothing to commit" in captured.out

def test_missing_commit_message(monkeypatch, capsys):
    exit_code = run_cli(monkeypatch, ["commit"])

    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Usage" in captured.out

def test_full_add_and_commit_flow(tmp_path, monkeypatch, capsys):
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