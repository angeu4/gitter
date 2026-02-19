import re


def test_branch_list(tmp_path, monkeypatch, capsys, run_cli):
    monkeypatch.chdir(tmp_path)

    run_cli(monkeypatch, ["init"])

    exit_code = run_cli(monkeypatch, ["branch"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "* main" in captured.out


def test_branch_create(tmp_path, monkeypatch, capsys, run_cli):
    monkeypatch.chdir(tmp_path)

    run_cli(monkeypatch, ["init"])

    exit_code = run_cli(monkeypatch, ["branch", "feature"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "created" in captured.out

    exit_code = run_cli(monkeypatch, ["branch"])
    captured = capsys.readouterr()

    assert "feature" in captured.out


def test_branch_duplicate(tmp_path, monkeypatch, capsys, run_cli):
    monkeypatch.chdir(tmp_path)

    run_cli(monkeypatch, ["init"])

    run_cli(monkeypatch, ["branch", "feature"])

    exit_code = run_cli(monkeypatch, ["branch", "feature"])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "already exists" in captured.out


def test_branch_list_default_regex(monkeypatch, capsys, run_cli, tmp_path):
    monkeypatch.chdir(tmp_path)

    run_cli(monkeypatch, ["init"])
    capsys.readouterr()

    exit_code = run_cli(monkeypatch, ["branch"])
    captured = capsys.readouterr()

    assert exit_code == 0

    pattern = r"^\* main\n$"
    assert re.fullmatch(pattern, captured.out)


def test_branch_create_regex(monkeypatch, capsys, run_cli, tmp_path):
    monkeypatch.chdir(tmp_path)

    run_cli(monkeypatch, ["init"])
    capsys.readouterr()

    exit_code = run_cli(monkeypatch, ["branch", "dev"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert re.fullmatch(r"Branch 'dev' created\n", captured.out)


def test_branch_list_multiple_regex(monkeypatch, capsys, run_cli, tmp_path):
    monkeypatch.chdir(tmp_path)

    run_cli(monkeypatch, ["init"])
    run_cli(monkeypatch, ["branch", "dev"])
    capsys.readouterr()

    exit_code = run_cli(monkeypatch, ["branch"])
    captured = capsys.readouterr()

    assert exit_code == 0

    pattern = r"^\* main\n  dev\n$|^  dev\n\* main\n$"
    assert re.fullmatch(pattern, captured.out)
