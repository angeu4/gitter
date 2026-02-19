import re


def test_add_without_repo_fails(tmp_path, monkeypatch, capsys, run_cli):
    monkeypatch.chdir(tmp_path)

    exit_code = run_cli(monkeypatch, ["add", "file.txt"])

    captured = capsys.readouterr()

    assert exit_code == 1
    assert "Not a gitter repository" in captured.out


def test_add_status_regex(monkeypatch, capsys, run_cli, tmp_path):
    monkeypatch.chdir(tmp_path)

    run_cli(monkeypatch, ["init"])
    capsys.readouterr()

    (tmp_path / "file1.txt").write_text("x")
    (tmp_path / "file2.md").write_text("x")

    run_cli(monkeypatch, ["add", "*.md"])
    capsys.readouterr()

    _ = run_cli(monkeypatch, ["status"])
    captured = capsys.readouterr()

    pattern = (
        r"^Changes\s+to\s+be\s+committed:\n"
        r"\s+new\s+file:\s+\S+\n"
        r"(?:\nUntracked\s+files:\n\s+\S+\n)?$"
    )

    assert re.search(pattern, captured.out)
