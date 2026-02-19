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


def test_log_regex(monkeypatch, capsys, run_cli, tmp_path):
    monkeypatch.chdir(tmp_path)

    run_cli(monkeypatch, ["init"])
    capsys.readouterr()

    (tmp_path / "file.md").write_text("x")
    run_cli(monkeypatch, ["add", "*.md"])
    run_cli(monkeypatch, ["commit", "-m", "adds file"])
    capsys.readouterr()

    _ = run_cli(monkeypatch, ["log"])
    captured = capsys.readouterr()

    pattern = (
        r"^commit\s+([0-9a-f]{40})(?:\s*//.*)?\s*\r?\n"
        r"Author:\s*(.*?)\s*\r?\n"
        r"Date:\s*(.*?)\s*\r?\n"
        r"\r?\n"
        r"([\s\S]*?)(?=^commit\s+[0-9a-f]{40}|\Z)"
    )

    assert re.search(pattern, captured.out, re.MULTILINE)


def test_log_empty_regex(monkeypatch, capsys, run_cli, tmp_path):
    monkeypatch.chdir(tmp_path)

    run_cli(monkeypatch, ["init"])
    capsys.readouterr()

    _ = run_cli(monkeypatch, ["log"])
    captured = capsys.readouterr()

    assert captured.out == ""
