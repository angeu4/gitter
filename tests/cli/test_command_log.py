import re


def test_log_no_commits(tmp_path, monkeypatch, capsys, run_cli):
    monkeypatch.chdir(tmp_path)

    run_cli(monkeypatch, ["init"])
    capsys.readouterr()  # flush init output

    exit_code = run_cli(monkeypatch, ["log"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert captured.out == ""

def test_log_single_commit(tmp_path, monkeypatch, capsys, run_cli):
    monkeypatch.chdir(tmp_path)

    run_cli(monkeypatch, ["init"])
    capsys.readouterr()

    file = tmp_path / "file.txt"
    file.write_text("hello")

    run_cli(monkeypatch, ["add", "file.txt"])
    capsys.readouterr()

    run_cli(monkeypatch, ["commit", "-m", "first"])
    capsys.readouterr()

    exit_code = run_cli(monkeypatch, ["log"])
    captured = capsys.readouterr()

    assert exit_code == 0

    output = captured.out

    assert re.search(r"^commit [0-9a-f]{40}", output, re.MULTILINE)
    assert "Author:" in output
    assert "Date:" in output
    assert "    first" in output


def test_log_multiple_commits(tmp_path, monkeypatch, capsys, run_cli):
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

    exit_code = run_cli(monkeypatch, ["log"])
    captured = capsys.readouterr()

    assert exit_code == 0

    output = captured.out

    assert "second" in output
    assert "first" in output

    # second should appear before first
    assert output.index("second") < output.index("first")
